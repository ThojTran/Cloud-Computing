from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.customer_service import (
    get_all_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    bulk_delete_customers,
)

customers_bp = Blueprint("customers", __name__)


#  LIST ALL 
@customers_bp.route("", methods=["GET"])
@jwt_required()
def list_customers():
    """
    GET /api/customers
    Trả về tất cả customers của user hiện tại.
    """
    user_id = int(get_jwt_identity())
    customers = get_all_customers(user_id)
    return jsonify({"customers": customers}), 200


# GET ONE 
@customers_bp.route("/<int:customer_id>", methods=["GET"])
@jwt_required()
def get_customer(customer_id):
    """
    GET /api/customers/<id>
    Trả về thông tin 1 customer.
    """
    user_id = int(get_jwt_identity())

    try:
        customer = get_customer_by_id(user_id, customer_id)
        return jsonify({"customer": customer}), 200
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
    user_id = int(get_jwt_identity())
    data = request.get_json()

    ids = data.get("ids", [])
    if not ids or not isinstance(ids, list):
        return jsonify({"error": "ids phải là danh sách không rỗng"}), 400

    try:
        count = bulk_delete_customers(user_id, ids)
        return jsonify({"message": f"Đã xóa {count} customers", "deleted": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# CREATE
@customers_bp.route("", methods=["POST"])
@jwt_required()
def add_customer():
    """
    POST /api/customers
    Body: { "full_name": "...", "phone": "...", "email": "...", "address": "..." }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data or not data.get("full_name", "").strip():
        return jsonify({"error": "full_name là bắt buộc"}), 400

    try:
        customer = create_customer(user_id, data)
        return jsonify({"message": "Tạo customer thành công", "customer": customer}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE 
@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@jwt_required()
def edit_customer(customer_id):
    """
    PUT /api/customers/<id>
    Body: { "full_name": "...", "phone": "...", ... } (chỉ gửi field cần sửa)
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    try:
        customer = update_customer(user_id, customer_id, data)
        return jsonify({"message": "Cập nhật thành công", "customer": customer}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# DELETE 
@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@jwt_required()
def remove_customer(customer_id):
    """
    DELETE /api/customers/<id>
    """
    user_id = int(get_jwt_identity())

    try:
        delete_customer(user_id, customer_id)
        return jsonify({"message": "Xóa customer thành công"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
