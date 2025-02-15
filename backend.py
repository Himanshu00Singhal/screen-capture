from flask import Flask, request, jsonify, render_template
import base64
import pytesseract
from PIL import Image
import io

app = Flask(__name__, template_folder="templates", static_folder="static")

# Store extracted text
extracted_text = {}

@app.route('/capture')
def capture_screen():
    return render_template("index.html")

@app.route('/process_image', methods=['POST'])
def process_image():
    global extracted_text
    data = request.json
    image_data = data.get("image")
    
    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # Convert Base64 image to PIL Image
    image_bytes = base64.b64decode(image_data.split(",")[1])
    image = Image.open(io.BytesIO(image_bytes))

    # Perform OCR
    text = pytesseract.image_to_string(image)
    extracted_text = {"captured_text": text}

    return jsonify(extracted_text)

@app.route('/get_text', methods=['GET'])
def get_text():
    return jsonify(extracted_text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
