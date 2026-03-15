from app.extensions import db
from app.models.customer import Customer


def get_all_customers(user_id: int) -> list:
    """Lấy tất cả customers của user hiện tại."""
    customers = Customer.query.filter_by(user_id=user_id).all()
    return [c.to_dict() for c in customers]


def get_customer_by_id(user_id: int, customer_id: int) -> dict:
    """Lấy 1 customer theo ID (chỉ trong phạm vi user đó)."""
    customer = Customer.query.filter_by(
        id=customer_id, user_id=user_id
    ).first()

    if not customer:
        raise ValueError("Không tìm thấy customer")

    return customer.to_dict()


def create_customer(user_id: int, data: dict) -> dict:
    """
    Tạo customer mới.
    data cần có: full_name (bắt buộc), phone, email, address (tuỳ chọn)
    """
    customer = Customer(
        user_id=user_id,
        full_name=data["full_name"],
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
    )

    db.session.add(customer)
    db.session.commit()

    return customer.to_dict()


def update_customer(user_id: int, customer_id: int, data: dict) -> dict:
    """Cập nhật thông tin customer."""
    customer = Customer.query.filter_by(
        id=customer_id, user_id=user_id
    ).first()

    if not customer:
        raise ValueError("Không tìm thấy customer")

    # Chỉ update những field được gửi lên
    if "full_name" in data:
        customer.full_name = data["full_name"]
    if "phone" in data:
        customer.phone = data["phone"]
    if "email" in data:
        customer.email = data["email"]
    if "address" in data:
        customer.address = data["address"]

    db.session.commit()

    return customer.to_dict()


def delete_customer(user_id: int, customer_id: int) -> None:
    """Xóa customer."""
    customer = Customer.query.filter_by(
        id=customer_id, user_id=user_id
    ).first()

    if not customer:
        raise ValueError("Không tìm thấy customer")

    db.session.delete(customer)
    db.session.commit()


def bulk_delete_customers(user_id: int, customer_ids: list) -> int:
    count = Customer.query.filter(
        Customer.id.in_(customer_ids),
        Customer.user_id == user_id,
    ).delete(synchronize_session=False)
                                        
    db.session.commit()
    return count
