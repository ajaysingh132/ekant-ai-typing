@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Ekant AI Typing</title>
</head>
<body>

<h1>🚀 Ekant AI Typing System</h1>

<!-- 🎤 Voice -->
<h2>🎤 Voice Typing</h2>
<button onclick="start()">Start Speaking</button>
<p id="voice_output"></p>

<!-- 📸 OCR -->
<h2>📸 Image / Handwriting → Text</h2>
<input type="file" id="imageInput">
<button onclick="upload()">Convert to Text</button>
<p id="ocr_output"></p>

<script>
// 🎤 Voice
function start() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "hi-IN";

    recognition.onresult = function(event) {
        document.getElementById("voice_output").innerText =
            event.results[0][0].transcript;
    };

    recognition.start();
}

// 📸 OCR
async function upload() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("/ocr", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    document.getElementById("ocr_output").innerText = data.text;
}
</script>

</body>
</html>
"""
