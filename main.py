from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

API_KEY = "helloworld"  # free key (testing)

@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    data = await file.read()

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"file": data},
        data={"apikey": API_KEY, "language": "eng"}
    )

    result = response.json()

    try:
        text = result["ParsedResults"][0]["ParsedText"]
    except:
        text = "Error reading text"

    return {"text": text}


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
