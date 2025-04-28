from flask import Flask, request, jsonify
import pytesseract
import re
from PIL import Image
import io

app = Flask(__name__)

# Aadhaar number pattern: 12 digits, often grouped as 4-4-4
AADHAAR_REGEX = r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b'

# Optional: If Tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update path if needed

@app.route('/extract_aadhaar', methods=['POST'])
def extract_aadhaar():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "Empty file uploaded."}), 400

    try:
        image = Image.open(io.BytesIO(image_file.read()))
        text = pytesseract.image_to_string(image)

        # Find Aadhaar numbers
        aadhaar_numbers = re.findall(AADHAAR_REGEX, text)
        aadhaar_numbers = [num.replace(' ', '') for num in aadhaar_numbers]  # Normalize

        if not aadhaar_numbers:
            return jsonify({"message": "No Aadhaar number found."}), 404

        return jsonify({"aadhaar_numbers": aadhaar_numbers}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
