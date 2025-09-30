from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return {"message": "PDF to PNG API is running 🚀"}
