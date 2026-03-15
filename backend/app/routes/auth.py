from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import register_user, login_user
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


# REGISTER 
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/user/register
    Body: { "email": "...", "username": "...", "password": "..." }
    """
    data = request.get_json()

    # Validate required fields
    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    email    = data.get("email", "").strip()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not email or not username or not password:
        return jsonify({"error": "email, username, password là bắt buộc"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password phải ít nhất 6 ký tự"}), 400

    try:
        user = register_user(email, username, password)
        return jsonify({"message": "Đăng ký thành công", "user": user}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


# LOGIN 
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/user/login
    Body: { "email": "...", "password": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    email    = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "email và password là bắt buộc"}), 400

    try:
        result = login_user(email, password)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401


# GET CURRENT USER 
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """
    GET /api/user/me
    Header: Authorization: Bearer <token>
    """
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"error": "User không tồn tại"}), 404

    return jsonify({"user": user.to_dict()}), 200
