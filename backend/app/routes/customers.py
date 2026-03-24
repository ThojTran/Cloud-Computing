from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    bulk_delete_customers,
)

customers_bp = Blueprint("customers", __name__)


def _get_current_user() -> User:
    """
    Load User object từ JWT identity.
    Raise LookupError nếu user không tồn tại trong DB.
    """
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        raise LookupError("User không tồn tại")
    return user


# LIST ALL
@customers_bp.route("", methods=["GET"])
@jwt_required()
def list_customers():
    """
    GET /api/customers
    Trả về tất cả customers thuộc org của user hiện tại.
    """
    try:
        user = _get_current_user()
        customers = get_all_customers(user)
        return jsonify({"customers": customers}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        # User chưa join org
        return jsonify({"error": str(e)}), 403


# GET ONE
@customers_bp.route("/<int:customer_id>", methods=["GET"])
@jwt_required()
def get_customer(customer_id):
    """
    GET /api/customers/<id>
    Trả về thông tin 1 customer trong org.
    """
    try:
        user = _get_current_user()
        customer = get_customer_by_id(user, customer_id)
        return jsonify({"customer": customer}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# BULK DELETE
@customers_bp.route("/bulk-delete", methods=["POST"])
@jwt_required()
def bulk_delete():
    """
    POST /api/customers/bulk-delete
    Body: { "ids": [1, 2, 3] }
    """
    data = request.get_json()
    ids = (data or {}).get("ids", [])

    if not ids or not isinstance(ids, list):
        return jsonify({"error": "ids phải là danh sách không rỗng"}), 400

    try:
        user = _get_current_user()
        count = bulk_delete_customers(user, ids)
        return jsonify({"message": f"Đã xóa {count} customers", "deleted": count}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403


# CREATE
@customers_bp.route("", methods=["POST"])
@jwt_required()
def add_customer():
    """
    POST /api/customers
    Body: { "full_name": "...", "phone": "...", "email": "...", "address": "..." }
    """
    data = request.get_json()

    if not data or not data.get("full_name", "").strip():
        return jsonify({"error": "full_name là bắt buộc"}), 400

    try:
        user = _get_current_user()
        customer = create_customer(user, data)
        return jsonify({"message": "Tạo customer thành công", "customer": customer}), 201
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 403


# UPDATE
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@jwt_required()
def edit_customer(customer_id):
    """
    PUT /api/customers/<id>
    Body: { "full_name": "...", "phone": "...", ... } (chỉ gửi field cần sửa)
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    try:
        user = _get_current_user()
        customer = update_customer(user, customer_id, data)
        return jsonify({"message": "Cập nhật thành công", "customer": customer}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# DELETE
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@jwt_required()
def remove_customer(customer_id):
    """
    DELETE /api/customers/<id>
    """
    try:
        user = _get_current_user()
        delete_customer(user, customer_id)
        return jsonify({"message": "Xóa customer thành công"}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 404