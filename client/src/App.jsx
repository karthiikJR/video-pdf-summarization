import { useState } from "react";

import "./App.css";
import Layout from "./components/Layout";
import Link from "./components/Link";
import PDFInput from "./components/PDFInput";
import Summary from "./components/Summary";
import EmbedVideo from "./components/EmbedVideo";
import Spinner from "./components/Spinner";

function App() {
  function convertToEmbedLink(youtubeLink) {
    let videoId;
    if (youtubeLink.includes("youtube.com")) {
      // Extract video ID from regular YouTube link
      const urlParams = new URLSearchParams(youtubeLink.split("?")[1]);
      videoId = urlParams.get("v");
    } else if (youtubeLink.includes("youtu.be")) {
      // Extract video ID from shortened YouTube link
      videoId = youtubeLink.split("/").pop().split("?")[0];
    } else {
      return "Invalid YouTube link";
    }
    // Construct the embed link
    const embedLink = `https://www.youtube.com/embed/${videoId}`;
    return embedLink;
  }

  const [isLoading, setIsLoading] = useState(false);
  const onSubmit = (e) => {
    e.preventDefault();
    const pdf = document.getElementById("dropzone-file");
    const url = document.getElementById("website-url");
    if (pdf.files[0] === undefined && url.value === "") {
      alert("Please upload a PDF or enter a URL");
      return;
    }

    setIsLoading(true);
    const summary = document.getElementById("summary");

    const embed = document.getElementById("embed");
    let youtubeLink = "";

    if (url.value !== "") {
      embed.src = convertToEmbedLink(url.value);
      youtubeLink = url.value;
    }

    if (youtubeLink === "") {
      const formData = new FormData();
      if (pdf.files[0] !== undefined) {
      } else {
        alert("Please upload a PDF or enter a URL");
        return;
      }
      formData.append("file", pdf.files[0]);
      console.log(formData.get("file"));
      fetch("http://127.0.0.1:5000/upload-pdf", {
        method: "POST",
        headers: {
          Accept: "*/*",
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.summary[0]);
          console.log(data.summary[0].summary_text);

          summary.textContent = data.summary[0].summary_text;
          setIsLoading(false);
        })
        .catch((error) => {
          console.error("Error:", error);
          setIsLoading(false);
        });
    } else {
      fetch("http://127.0.0.1:5000/generate-summary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Set the Content-Type header to indicate JSON data
        },
        body: JSON.stringify({
          // Serialize the request body as JSON
          video_link: youtubeLink,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);

          const summ = data.summary.split(". ");
          if (
            summ.length >= 2 &&
            summ[0].startsWith("This is a very short film") &&
            summ[1].startsWith("It does not advance our plot")
          ) {
            // Remove the first two summ
            summ.splice(0, 2);
          }

          summary.textContent = summ.join(". ");
          setIsLoading(false);
        })
        .catch((error) => {
          console.error("Error:", error);
          setIsLoading(false);
        });
    }
  };
  return (
    <Layout>
      <div className="w-full flex-1 flex flex-col gap-5">
        <div className="flex flex-wrap gap-2 items-end justify-between">
          <Link></Link>
          <button
            onClick={(e) => {
              onSubmit(e);
            }}
            className="text-white bg-emerald-600 sm:px-4 rounded-lg p-3"
          >
            Generate
          </button>
        </div>
        <PDFInput></PDFInput>
        <EmbedVideo></EmbedVideo>
      </div>
      <div className="flex-1">
        <div className={isLoading ? "hidden" : ""}>
          <Summary></Summary>
        </div>
        <div className={isLoading ? "" : "hidden"}>
          <Spinner></Spinner>
        </div>
      </div>
    </Layout>
  );
}

export default App;
