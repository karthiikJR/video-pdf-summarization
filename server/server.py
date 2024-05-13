import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import sys
import json
import torch
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'uploads'
CORS(app)

whisper_models = ["small", "medium", "small.en", "medium.en"]
source_languages = {
    "en": "English",
    "zh": "Chinese",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
    "ko": "Korean",
    "fr": "French"
}
source_language_list = [key[0] for key in source_languages.items()]

# Download video .m4a and info.json
def get_youtube(video_url):
    import yt_dlp

    ydl_opts = {'format': 'bestaudio[ext=m4a]'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        info['title'] = info['title'].replace('$', '').replace('|', '-')
        abs_video_path = ydl.prepare_filename(info)
        with open(abs_video_path.replace('m4a', 'info.json'), 'w') as outfile:
            json.dump(info, outfile, indent=2)
        ydl.process_info(info)

    print("Success download", video_url, "to", abs_video_path)
    return abs_video_path

# Convert video .m4a into .wav
def convert_to_wav(video_file_path, offset=0):

    out_path = video_file_path.replace("m4a", "wav")
    if os.path.exists(out_path):
        print("wav file already exists:", out_path)
        return out_path

    try:
        print("starting conversion to wav")
        offset_args = f"-ss {offset}" if offset > 0 else ''
        os.system(f'ffmpeg {offset_args} -i "{video_file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{out_path}"')
        print("conversion to wav ready:", out_path)
    except Exception as e:
        raise RuntimeError("Error converting.")

    return out_path

# Transcribe .wav into .segments.json
def speech_to_text(video_file_path, selected_source_lang='en', whisper_model='small.en', vad_filter=False):
    print('loading faster_whisper model:', whisper_model)
    from faster_whisper import WhisperModel
    model = WhisperModel(whisper_model, device="cuda")
    if (video_file_path == None):
        raise ValueError("Error no video input")
    print(video_file_path)

    try:
        # Read and convert youtube video
        _, file_ending = os.path.splitext(f'{video_file_path}')
        audio_file = video_file_path.replace(file_ending, ".m4a")
        out_file = video_file_path.replace(file_ending, ".segments.json")
        if os.path.exists(out_file):
            print("segments file already exists:", out_file)
            with open(out_file) as f:
                segments = json.load(f)
            return segments

        # Transcribe audio
        print('starting transcription...')
        options = dict(language=selected_source_lang, beam_size=5, best_of=5, vad_filter=vad_filter)
        transcribe_options = dict(task="transcribe", **options)

        segments_raw, info = model.transcribe(audio_file, **transcribe_options)

        # Convert back to original openai format
        segments = []
        i = 0
        for segment_chunk in segments_raw:
            chunk = {}
            chunk["start"] = segment_chunk.start
            chunk["end"] = segment_chunk.end
            chunk["text"] = segment_chunk.text
            print(chunk)
            segments.append(chunk)
            i += 1
        print("transcribe audio done with fast whisper")

        with open(out_file, 'w') as f:
            f.write(json.dumps(segments, indent=2))

    except Exception as e:
        raise RuntimeError("Error transcribing.")
    return segments


def extract_video_id(video_link):
    # Split the video link by '=' and take the last part
    return video_link.split('=')[-1]

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def summarize(large_text):
    hf_name = 'pszemraj/led-large-book-summary'
    summarizer = pipeline(
        "summarization",
        hf_name,
        device=0 if torch.cuda.is_available() else -1,
    )

    wall_of_text = large_text

    result = summarizer(
        wall_of_text,
        min_length=16,
        max_length=256,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=3,
        repetition_penalty=3.5,
        num_beams=4,
        early_stopping=True,
    )

    return result

# Function to split text into chunks but keep same lines in 2 parts at the end and start
def split_keep_context(text):
    lines = text.split('\n')
    chunk_size = 16384
    chunk_texts = []
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line + '\n'
        else:
            chunk_texts.append(current_chunk)
            current_chunk = line + '\n'
    if current_chunk:
        chunk_texts.append(current_chunk)
    return chunk_texts

def read_subtitle_json(file_path):
    try:
        with open(file_path, 'r') as file:
            subtitles = json.load(file)
            return subtitles
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        sys.exit(1)

def merge_subtitles_to_paragraph(subtitles):
    paragraph = ""
    for subtitle in subtitles:
        paragraph += subtitle['text'] + ' '
    return paragraph.strip()

def save_transcript_to_json(transcript, output_file):
    try:
        # Write transcript to a JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(transcript, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving transcript to JSON: {str(e)}")
        sys.exit(1)

def extract_text_from_pdf(pdf_path):
    text = ""
    images = []

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Extract text from the page
        page_text = page.get_text()
        # Remove excessive empty lines
        page_text = "\n".join([line.strip() for line in page_text.splitlines() if line.strip()])
        text += page_text + "\n"

        # Extract images from the page
        images += page.get_images(full=True)

    pdf_document.close()

    if text.strip() == "":
        # If there is no text, perform OCR on the images
        for img_index, img_info in enumerate(images):
            xref = img_info[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_text = pytesseract.image_to_string(image)
            # Remove excessive empty lines
            image_text = "\n".join([line.strip() for line in image_text.splitlines() if line.strip()])
            text += "\n\n[Image {}]\n\n".format(img_index + 1)
            text += image_text + "\n"

    return text.strip()

@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    # Get video link from POST request
    video_link = request.json.get('video_link')

    if not video_link:
        return jsonify({'error': 'Video link not provided'}), 400

    # Extract video ID from the link
    video_id = extract_video_id(video_link)

    try:
        # Fetch transcript using the original method
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        save_transcript_to_json(transcript, 'transcript.json')

    except Exception as e:
        print(f"Error fetching transcript using the original method: {e}")

        try:
            # Define the YouTube link you want to process
            yt_link = video_link

            # Download the video from the provided link
            video_path = get_youtube(yt_link)

            # Convert the downloaded video to WAV format
            convert_to_wav(video_path)

            # Transcribe the WAV file
            segments = speech_to_text(video_path)

            # Define the output file path
            output_file = video_path.replace(".m4a", ".segments.json")

            # Save the transcript to a JSON file
            save_transcript_to_json(segments, 'transcript.json')

        except Exception as e:
            return jsonify({'error': f'Both transcript methods failed: {e}'}), 500

    try:
        # Get the directory of the current script file
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Construct the file path relative to the current directory
        file_path = os.path.join(current_directory, 'transcript.json')

        subtitles = read_subtitle_json(file_path)

        paragraph = merge_subtitles_to_paragraph(subtitles)

        summary = summarize(paragraph)
        chunk_texts = split_keep_context(paragraph)

        summaries = []
        for chunk_text in chunk_texts:
            summary = summarize(chunk_text)
            summaries.append(summary)

        combined_summary = ""
        for i, summary in enumerate(summaries):
            combined_summary += summary[0]['summary_text'] + " "

        print(combined_summary)

        # Write the summary to a file
        with open('summary.txt', 'w') as file:
            file.write(combined_summary)

        # Read the output summary
        with open('summary.txt', 'r') as file:
            summary = file.read()

        return jsonify({'summary': summary}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # Check if the POST request has the file part
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from the PDF file
        extracted_text = extract_text_from_pdf(file_path)
        
        # Generate summary from the extracted text
        summary = summarize(extracted_text)

        return jsonify({'summary': summary}), 200

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
