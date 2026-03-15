from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

#khởi tạo extensions
db = SQLAlchemy()
jwt = JWTManager() #tạo và xác nhận JWT token khi đăng nhập
cors = CORS() # CORS để cho phép frontend (React) truy cập API từ domain khác, chỉ định các origin cụ thể để bảo mật hơn
migrate = Migrate() # uppdate database khi mà model thay đổi