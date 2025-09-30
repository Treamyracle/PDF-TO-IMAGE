from flask import Flask
from flask_cors import CORS
from routes import home_bp, convert_bp, ocr_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(convert_bp)
app.register_blueprint(ocr_bp)

# Penting untuk Vercel: jangan pakai app.run()
# if __name__ == "__main__":
#     app.run(debug=True)
