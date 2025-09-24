from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # <-- 1. IMPORT CORS
import fitz  # PyMuPDF
import io
import tempfile
import os

app = Flask(__name__)
CORS(app)  # <-- 2. INISIALISASI CORS UNTUK SELURUH APLIKASI

@app.route("/")
def home():
    return {"message": "PDF to PNG API is running 🚀"}

@app.route("/convert", methods=["POST"])
def convert_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["file"]
    
    # Simpan PDF sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        doc = fitz.open(tmp_path)
        images = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            img_io = io.BytesIO(img_bytes)
            img_io.seek(0)
            images.append((f"page_{page_num+1}.png", img_io))

        # Jika hanya 1 halaman, kirim sebagai PNG
        if len(images) == 1:
            return send_file(images[0][1], mimetype="image/png")

        # Jika lebih dari 1 halaman, kirim sebagai ZIP
        zip_io = io.BytesIO()
        import zipfile
        with zipfile.ZipFile(zip_io, mode="w") as zf:
            for filename, img_io in images:
                zf.writestr(filename, img_io.getvalue())
        zip_io.seek(0)

        return send_file(
            zip_io,
            mimetype="application/zip",
            as_attachment=True,
            download_name="converted_images.zip"
        )
    finally:
        # Pastikan file sementara selalu dihapus
        os.remove(tmp_path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
