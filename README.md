# Summarization Website

This repository contains the code for a summarization website that can generate summaries from either YouTube videos or PDF files. The backend is built using Flask, while the frontend is developed with React. The project utilizes several machine learning models and libraries to perform tasks such as transcription, translation, and summarization.

## Table of Contents

- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Libraries Used](#libraries-used)
- [Methodology](#methodology)
- [Screenshots](#screenshots)

## Features

- Summarize YouTube videos by extracting the transcript and generating a summary.
- Summarize PDF files by extracting text and generating a summary.
- Seamless integration between the backend and frontend.
- Provides a clean and user-friendly interface.

## Setup and Installation

### Backend

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/summarization-website.git
    cd summarization-website
    ```
2. **Create a `requirements.txt` file with the following content:**
    ```plaintext
    Flask==2.0.1
    flask-cors==3.0.10
    torch==2.0.1
    transformers==4.28.1
    yt-dlp==2021.12.1
    youtube-transcript-api==0.4.4
    faster-whisper==0.2.3
    pymupdf==1.19.6
    pytesseract==0.3.8
    Pillow==9.0.1
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Flask application:**
    ```sh
    flask --app server run
    ```

### Frontend

1. **Navigate to the `frontend` directory:**
    ```sh
    cd frontend
    ```

2. **Install the dependencies:**
    ```sh
    npm install
    ```

3. **Start the React application:**
    ```sh
    npm run dev
    ```

## Usage

1. **Access the website:**
   Open your browser and go to `http://localhost:3000` to access the summarization website.

2. **Summarize a YouTube video:**
   - Enter the YouTube video link in the provided input field.
   - Click the "Generate" button to fetch the transcript and generate a summary.

3. **Summarize a PDF file:**
   - Upload a PDF file using the file input field.
   - Click the "Generate" button to extract text from the PDF and generate a summary.

## API Endpoints

### `POST /generate-summary`

Generates a summary from a YouTube video.

- **Request Body:**
    ```json
    {
      "video_link": "https://www.youtube.com/watch?v=your_video_id"
    }
    ```

- **Response:**
    ```json
    {
      "summary": "Summary of the video."
    }
    ```

### `POST /upload-pdf`

Generates a summary from a PDF file.

- **Request:**
  - Multipart/form-data with the PDF file.

- **Response:**
    ```json
    {
      "summary": "Summary of the PDF."
    }
    ```

## Frontend Components

- **App.js:** Main component that handles the state and logic for generating summaries.
- **PDFInput.js:** Component for uploading PDF files.
- **Link.js:** Component for inputting YouTube video links.
- **Summary.js:** Component for displaying the generated summary.
- **EmbedVideo.js:** Component for embedding the YouTube video.
- **Spinner.js:** Component for displaying a loading spinner.

## Libraries Used

### Backend

- **Flask:** Web framework for building the backend.
- **Flask-CORS:** Extension for handling Cross-Origin Resource Sharing (CORS).
- **Torch:** Machine learning library for deep learning models.
- **Transformers:** Library for natural language processing models.
- **yt-dlp:** YouTube video downloader.
- **youtube-transcript-api:** API for fetching YouTube video transcripts.
- **faster-whisper:** Library for faster Whisper model inference.
- **PyMuPDF:** Library for PDF processing.
- **pytesseract:** OCR tool for extracting text from images.
- **Pillow:** Imaging library for Python.

### Frontend

- **React:** JavaScript library for building user interfaces.
- **React-DOM:** Package for working with the DOM in React applications.
- **Tailwind CSS:** Utility first CSS framework
- **React Spinner:** Package for adding a spinner  

## Methodology

The methodology for generating summaries from YouTube videos or PDF documents involves several steps, as illustrated in the following flowchart:

![Methodology Flowchart](https://github.com/karthiikJR/video-pdf-summarization/assets/115890844/87e23258-3660-4222-9555-47bb15ba9aac)


### Workflow:

1. **User Interface for Input:**
   - The user provides a YouTube link or uploads a PDF document through the user interface.

2. **YouTube Video Processing:**
   - If a YouTube link is provided, the system checks if a transcript is available:
     - **Yes:** The transcript is cleaned up using spaCy.
     - **No:** The audio is downloaded and transcribed using Whisper.

3. **PDF Document Processing:**
   - If a PDF document is uploaded, the system checks if the text is selectable:
     - **Yes:** Text is extracted directly from the PDF.
     - **No:** The PDF is scanned and text is extracted using OCR.

4. **Text Processing:**
   - The extracted text (from YouTube or PDF) is chunked into smaller parts for easier processing.

5. **Summarization:**
   - Each chunk is summarized individually using the summarization model.

6. **Summary Cleanup:**
   - The individual summaries are concatenated and cleaned up to form the final summary.

7. **Output:**
   - The final generated summary is outputted to the user.

This structured approach ensures that the system can handle different types of input and generate coherent summaries effectively.

## Screenshots

### Home Screen

![Screenshot 2024-05-01 233244](https://github.com/karthiikJR/video-pdf-summarization/assets/115890844/f3667d78-2e5f-4b99-a809-e54fac716e33)

### Summary from YT Link

![Screenshot 2024-05-01 233519](https://github.com/karthiikJR/video-pdf-summarization/assets/115890844/8dc5ac38-1ee6-4d45-8bb5-e5b7b855fd47)

## Summary for PDF

![Screenshot 2024-05-01 233641](https://github.com/karthiikJR/video-pdf-summarization/assets/115890844/89e68f42-b123-40de-8fcf-4e3f0e8502ea)


---
