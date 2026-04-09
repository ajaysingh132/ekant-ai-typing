from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from PIL import Image
import io
import numpy as np
import easyocr

app = FastAPI()

# OCR Reader
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}

# OCR API
@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))
    image = np.array(image)

    result = reader.readtext(image, detail=0)

    text = " ".join(result)

    return {"text": text}


# UI
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <h1>🚀 AI Typing System</h1>

    <h2>🎤 Voice</h2>
    <button onclick="start()">Start Speaking</button>
    <p id="voice"></p>

    <h2>📷 OCR (Photo / Handwriting)</h2>
    <input type="file" id="file">
    <button onclick="upload()">Convert</button>
    <p id="ocr"></p>

    <script>
    function start() {
        const r = new webkitSpeechRecognition();
        r.lang = "hi-IN";
        r.onresult = e => {
            document.getElementById("voice").innerText =
                e.results[0][0].transcript;
        };
        r.start();
    }

    async function upload() {
        let file = document.getElementById("file").files[0];

        let formData = new FormData();
        formData.append("file", file);

        let res = await fetch("/ocr", {
            method: "POST",
            body: formData
        });

        let data = await res.json();
        document.getElementById("ocr").innerText = data.text;
    }
    </script>
    """
