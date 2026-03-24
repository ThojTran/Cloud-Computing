from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token
import secrets
from app.models.Organization import Organization


def register_user(email: str, username: str, password: str) -> dict:
    # Kiểm tra email/username đã tồn tại chưa
    if User.query.filter_by(email=email).first():
        raise ValueError("Email đã được sử dụng")
    if User.query.filter_by(username=username).first():
        raise ValueError("Username đã được sử dụng")

    user = User(email=email, username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user.to_dict()


def login_user(email: str, password: str) -> dict:
    """
    Đăng nhập user.
    Trả về JWT access_token nếu hợp lệ, raise ValueError nếu sai.
    """
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        raise ValueError("Email hoặc mật khẩu không đúng")

    # Tạo JWT token – identity là user.id
    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user": user.to_dict(),
    }
    # tạo 1 group
def register_org(org_name: str, email: str, username: str, password: str) -> dict:
    """Tạo org mới + user admin cùng lúc."""
    if User.query.filter_by(email=email).first():
        raise ValueError("Email đã được sử dụng")
    if User.query.filter_by(username=username).first():
        raise ValueError("Username đã được sử dụng")

    # Tạo invite_code ngẫu nhiên, đảm bảo unique
    while True:
        code = secrets.token_urlsafe(10)
        if not Organization.query.filter_by(invite_code=code).first():
            break

    org = Organization(name=org_name, invite_code=code)
    db.session.add(org)
    db.session.flush()  # lấy org.id

    user = User(email=email, username=username, org_id=org.id, role="admin")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"org_id": org.id, "invite_code": org.invite_code, "user": user.to_dict()}


def join_org(user_id: int, invite_code: str) -> dict:
    """User chưa có org nhập invite code để join."""
    user = User.query.get(user_id)

    if user.org_id is not None:
        raise ValueError("Bạn đã thuộc một org rồi")

    org = Organization.query.filter_by(invite_code=invite_code).first()
    if not org:
        raise ValueError("Invite code không hợp lệ")

    user.org_id = org.id
    user.role = "member"
    db.session.commit()

    return {"org_id": org.id, "org_name": org.name, "user": user.to_dict()}
