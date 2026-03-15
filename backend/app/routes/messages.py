from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.message_service import send_message, get_message_history

messages_bp = Blueprint("messages", __name__)


# SEND MESSAGE 
@messages_bp.route("/send", methods=["POST"])
@jwt_required()
def send():
    """
    POST /api/messages/send
    Body: {
        "type": "sms" | "email",
        "subject": "..." (bắt buộc nếu type=email),
        "content": "...",
        "customer_ids": [1, 2, 3]
    }

    Gửi SMS hoặc Email cho 1 hoặc nhiều customers.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body không được trống"}), 400

    msg_type     = data.get("type", "").strip()
    subject      = data.get("subject", "").strip()
    content      = data.get("content", "").strip()
    customer_ids = data.get("customer_ids", [])

    # Validation
    if msg_type not in ("sms", "email"):
        return jsonify({"error": "type phải là 'sms' hoặc 'email'"}), 400

    if not content:
        return jsonify({"error": "content là bắt buộc"}), 400

    if msg_type == "email" and not subject:
        return jsonify({"error": "subject là bắt buộc khi gửi email"}), 400

    if not customer_ids or not isinstance(customer_ids, list):
        return jsonify({"error": "customer_ids phải là danh sách không rỗng"}), 400

    try:
        result = send_message(user_id, msg_type, subject, content, customer_ids)
        return jsonify({"message": "Gửi thành công", "data": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# MESSAGE HISTORY 
@messages_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    """
    GET /api/messages/history
    Trả về lịch sử tất cả messages đã gửi.
    """
    user_id = int(get_jwt_identity())
    messages = get_message_history(user_id)
    return jsonify({"messages": messages}), 200
