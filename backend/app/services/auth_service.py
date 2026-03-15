from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token


def register_user(email: str, username: str, password: str) -> dict:
    """
    Đăng ký user mới.
    Trả về dict user nếu thành công, raise ValueError nếu trùng.
    """
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
