from app.extensions import db
from app.models.customer import Customer

def _get_org_id(user) -> int:
    """Helper — raise nếu user chưa join org."""
    if user.org_id is None:
        raise ValueError("Bạn chưa thuộc org nào")
    return user.org_id

def get_all_customers(user) -> list:
    org_id = _get_org_id(user)
    customers = Customer.query.filter_by(org_id=org_id).all()
    return [c.to_dict() for c in customers]


def get_customer_by_id(user, customer_id: int) -> dict:
    org_id = _get_org_id(user)
    customer = Customer.query.filter_by(id=customer_id, org_id=org_id).first()
    if not customer:
        raise ValueError("Không tìm thấy customer")
    return customer.to_dict()

def create_customer(user, data: dict) -> dict:
    """
    Tạo customer mới.
    data cần có: full_name (bắt buộc), phone, email, address (tuỳ chọn)
    """
    org_id = _get_org_id(user)
    customer = Customer(
        org_id=org_id,
        full_name=data["full_name"],
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
    )
    db.session.add(customer)
    db.session.commit()
    return customer.to_dict()


def update_customer(user, customer_id: int, data: dict) -> dict:
    """Cập nhật thông tin customer."""
    org_id = _get_org_id(user)
    customer = Customer.query.filter_by(id=customer_id, org_id=org_id).first()
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


def delete_customer(user: int, customer_id: int) -> None:
    """Xóa customer."""
    org_id = _get_org_id(user)
    customer = Customer.query.filter_by(id=customer_id, org_id=org_id).first()

    if not customer:
        raise ValueError("Không tìm thấy customer")

    db.session.delete(customer)
    db.session.commit()


def bulk_delete_customers(user: int, customer_ids: list) -> int:
    org_id = _get_org_id(user)
    count = Customer.query.filter(
        Customer.id.in_(customer_ids),
        Customer.org_id == org_id,
    ).delete(synchronize_session=False)
                                        
    db.session.commit()
    return count
