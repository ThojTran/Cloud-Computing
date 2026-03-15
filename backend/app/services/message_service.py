from app.extensions import db
from app.models.message import Message
from app.models.message_recip import MessageRecipient
from app.models.customer import Customer
from app.services.sms_service import send_sms
from app.services.email_service import send_email


def send_message(user_id: int, msg_type: str, subject: str,
                 content: str, customer_ids: list) -> dict:

    if msg_type not in ("sms", "email"):
        raise ValueError("type phải là 'sms' hoặc 'email'")

    if not customer_ids:
        raise ValueError("Phải chọn ít nhất 1 customer")

    # Validate: tất cả customer_ids phải thuộc về user hiện tại
    customers = Customer.query.filter(
        Customer.id.in_(customer_ids),
        Customer.user_id == user_id,
    ).all()

    if len(customers) != len(customer_ids):
        raise ValueError("Một số customer không tồn tại hoặc không thuộc về bạn")

    # Bước 1: Tạo Message record
    message = Message(
        user_id=user_id,
        type_ms=msg_type,
        subject=subject if msg_type == "email" else None,
        context_ms=content,
    )
    db.session.add(message)
    db.session.flush()  # Lấy message.id mà chưa commit

    # Bước 2: Gửi cho từng customer + tạo recipient records
    results = []
    for customer in customers:
        # Gọi service tương ứng
        if msg_type == "sms":
            if not customer.phone:
                result = {"success": False, "error": "Customer không có số điện thoại"}
            else:
                result = send_sms(customer.phone, content)
        else:  # email
            if not customer.email:
                result = {"success": False, "error": "Customer không có email"}
            else:
                result = send_email(customer.email, subject, content)

        # Tạo recipient record với status
        recipient = MessageRecipient(
            message_id=message.id,
            customer_id=customer.id,
            status="sent" if result["success"] else "failed",
        )
        db.session.add(recipient)

        entry = {
            "customer_id": customer.id,
            "customer_name": customer.full_name,
            "status": recipient.status,
        }
        if not result["success"]:
            entry["error"] = result.get("error")
        
        results.append(entry)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Lỗi lưu database: {str(e)}")

    return {
        "message": message.to_dict(),
        "results": results,
    }


def get_message_history(user_id: int) -> list:
    """Lấy lịch sử tất cả messages đã gửi bởi user."""
    messages = (
        Message.query
        .filter_by(user_id=user_id)
        .order_by(Message.sent_at.desc())
        .all()
    )
    return [m.to_dict() for m in messages]
