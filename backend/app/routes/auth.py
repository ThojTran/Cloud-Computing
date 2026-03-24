from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import register_user, login_user, register_org, join_org
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


# REGISTER USER
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    POST /api/auth/register
    Body: { "email": "...", "username": "...", "password": "..." }
    Đăng ký user mới, chưa thuộc org nào.
    """
    data = request.get_json()

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


# REGISTER ORG
@auth_bp.route("/register-org", methods=["POST"])
def register_organization():
    """
    POST /api/auth/register-org
    Body: { "org_name": "...", "email": "...", "username": "...", "password": "..." }
    Tạo org mới + user admin cùng lúc.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    org_name = data.get("org_name", "").strip()
    email    = data.get("email", "").strip()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not org_name or not email or not username or not password:
        return jsonify({"error": "org_name, email, username, password là bắt buộc"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password phải ít nhất 6 ký tự"}), 400

    try:
        result = register_org(org_name, email, username, password)
        return jsonify({"message": "Tạo org thành công", "data": result}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


# JOIN ORG
@auth_bp.route("/join-org", methods=["POST"])
@jwt_required()
def join_organization():
    """
    POST /api/auth/join-org
    Header: Authorization: Bearer <token>
    Body: { "invite_code": "..." }
    User chưa có org nhập invite code để join.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    invite_code = (data or {}).get("invite_code", "").strip()
    if not invite_code:
        return jsonify({"error": "invite_code là bắt buộc"}), 400

    try:
        result = join_org(user_id, invite_code)
        return jsonify({"message": "Join org thành công", "data": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /api/auth/login
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
    GET /api/auth/me
    Header: Authorization: Bearer <token>
    """
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"error": "User không tồn tại"}), 404

    return jsonify({"user": user.to_dict()}), 200