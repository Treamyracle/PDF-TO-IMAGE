from flask import Blueprint, request, jsonify
import cv2
import pytesseract
from PIL import Image
import numpy as np

ocr_bp = Blueprint("ocr", __name__)

def preprocess_image_bytes(image_bytes: bytes):
    # Baca gambar dari bytes
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Gambar tidak valid")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize sedikit agar teks lebih jelas
    scale = 1.5
    gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    # Denoise & thresholding
    gray = cv2.medianBlur(gray, 3)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return th

@ocr_bp.route("/ocr", methods=["POST"])
def ocr_endpoint():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["file"]
        lang = request.form.get("lang", "eng")

        image_bytes = file.read()
        pre = preprocess_image_bytes(image_bytes)

        # Convert numpy array → PIL
        pil_img = Image.fromarray(pre)

        # OCR
        text = pytesseract.image_to_string(pil_img, lang=lang)

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
