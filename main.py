from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ekant AI Typing Running 🚀"}

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Ekant AI Typing</title>
    </head>
    <body>

    <h1>🎤 Voice Typing System</h1>

    <button onclick="start()">Start Speaking</button>

    <p id="output"></p>

    <script>
    function start() {
      const recognition = new webkitSpeechRecognition();
      recognition.lang = "hi-IN";

      recognition.onresult = function(event) {
        document.getElementById("output").innerText =
          event.results[0][0].transcript;
      };

      recognition.start();
    }
    </script>

    </body>
    </html>
    """
