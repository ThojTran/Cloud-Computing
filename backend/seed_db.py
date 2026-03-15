from app import create_app
from app.extensions import db
from app.models.user import User
from app.services.auth_service import register_user
from app.services.customer_service import create_customer
import sys

app = create_app()

contacts = [
    {"full_name": "Nguyễn Văn An", "phone": "0901234001", "address": "Hà Nội", "email": "an.nguyen1@gmail.com"},
    {"full_name": "Trần Thị Bình", "phone": "0901234002", "address": "TP.HCM", "email": "binh.tran2@gmail.com"},
    {"full_name": "Lê Văn Cường", "phone": "0901234003", "address": "Đà Nẵng", "email": "cuong.le3@gmail.com"},
    {"full_name": "Phạm Thị Dung", "phone": "0901234004", "address": "Hải Phòng", "email": "dung.pham4@gmail.com"},
    {"full_name": "Hoàng Văn Đức", "phone": "0901234005", "address": "Cần Thơ", "email": "duc.hoang5@gmail.com"},
    {"full_name": "Vũ Thị Hạnh", "phone": "0901234006", "address": "Hà Nội", "email": "hanh.vu6@gmail.com"},
    {"full_name": "Đặng Văn Khánh", "phone": "0901234007", "address": "Bình Dương", "email": "khanh.dang7@gmail.com"},
    {"full_name": "Bùi Thị Lan", "phone": "0901234008", "address": "Đồng Nai", "email": "lan.bui8@gmail.com"},
    {"full_name": "Đỗ Văn Minh", "phone": "0901234009", "address": "Nghệ An", "email": "minh.do9@gmail.com"},
    {"full_name": "Hồ Thị Nga", "phone": "0901234010", "address": "Huế", "email": "nga.ho10@gmail.com"},
    {"full_name": "Phan Văn Nam", "phone": "0901234011", "address": "Quảng Nam", "email": "nam.phan11@gmail.com"},
    {"full_name": "Lý Thị Oanh", "phone": "0901234012", "address": "Hà Nội", "email": "oanh.ly12@gmail.com"},
    {"full_name": "Nguyễn Văn Phúc", "phone": "0901234013", "address": "TP.HCM", "email": "phuc.nguyen13@gmail.com"},
    {"full_name": "Trịnh Thị Quỳnh", "phone": "0901234014", "address": "Đà Nẵng", "email": "quynh.trinh14@gmail.com"},
    {"full_name": "Lê Văn Sơn", "phone": "0901234015", "address": "Hải Phòng", "email": "son.le15@gmail.com"},
    {"full_name": "Phạm Thị Trang", "phone": "0901234016", "address": "Hà Nội", "email": "trang.pham16@gmail.com"},
    {"full_name": "Hoàng Văn Tuấn", "phone": "0901234017", "address": "Bắc Ninh", "email": "tuan.hoang17@gmail.com"},
    {"full_name": "Vũ Thị Uyên", "phone": "0901234018", "address": "Hải Dương", "email": "uyen.vu18@gmail.com"},
    {"full_name": "Đặng Văn Vinh", "phone": "0901234019", "address": "Nam Định", "email": "vinh.dang19@gmail.com"},
    {"full_name": "Bùi Thị Yến", "phone": "0901234020", "address": "Hà Nội", "email": "yen.bui20@gmail.com"},
    {"full_name": "Đỗ Văn Anh", "phone": "0901234021", "address": "TP.HCM", "email": "anh.do21@gmail.com"},
    {"full_name": "Hồ Thị Bích", "phone": "0901234022", "address": "Cần Thơ", "email": "bich.ho22@gmail.com"},
    {"full_name": "Phan Văn Chiến", "phone": "0901234023", "address": "Đà Nẵng", "email": "chien.phan23@gmail.com"},
    {"full_name": "Lý Thị Diệu", "phone": "0901234024", "address": "Hà Nội", "email": "dieu.ly24@gmail.com"},
    {"full_name": "Nguyễn Văn Đông", "phone": "0901234025", "address": "Quảng Ninh", "email": "dong.nguyen25@gmail.com"},
    {"full_name": "Trần Thị Giang", "phone": "0901234026", "address": "Hải Phòng", "email": "giang.tran26@gmail.com"},
    {"full_name": "Lê Văn Hải", "phone": "0901234027", "address": "Hà Nội", "email": "hai.le27@gmail.com"},
    {"full_name": "Phạm Thị Hòa", "phone": "0901234028", "address": "Huế", "email": "hoa.pham28@gmail.com"},
    {"full_name": "Hoàng Văn Khoa", "phone": "0901234029", "address": "TP.HCM", "email": "khoa.hoang29@gmail.com"},
    {"full_name": "Vũ Thị Linh", "phone": "0901234030", "address": "Hà Nội", "email": "linh.vu30@gmail.com"},
    {"full_name": "Đặng Văn Long", "phone": "0901234031", "address": "Nghệ An", "email": "long.dang31@gmail.com"},
    {"full_name": "Bùi Thị Mai", "phone": "0901234032", "address": "Đà Nẵng", "email": "mai.bui32@gmail.com"},
    {"full_name": "Đỗ Văn Nam", "phone": "0901234033", "address": "Bình Dương", "email": "nam.do33@gmail.com"},
    {"full_name": "Hồ Thị Oanh", "phone": "0901234034", "address": "Đồng Nai", "email": "oanh.ho34@gmail.com"},
    {"full_name": "Phan Văn Phong", "phone": "0901234035", "address": "Hà Nội", "email": "phong.phan35@gmail.com"},
    {"full_name": "Lý Thị Quỳnh", "phone": "0901234036", "address": "TP.HCM", "email": "quynh.ly36@gmail.com"},
    {"full_name": "Nguyễn Văn Sơn", "phone": "0901234037", "address": "Hà Nội", "email": "son.nguyen37@gmail.com"},
    {"full_name": "Trần Thị Thảo", "phone": "0901234038", "address": "Hải Phòng", "email": "thao.tran38@gmail.com"},
    {"full_name": "Lê Văn Tùng", "phone": "0901234039", "address": "Đà Nẵng", "email": "tung.le39@gmail.com"},
    {"full_name": "Phạm Thị Uyên", "phone": "0901234040", "address": "Hà Nội", "email": "uyen.pham40@gmail.com"},
    {"full_name": "Hoàng Văn Vũ", "phone": "0901234041", "address": "TP.HCM", "email": "vu.hoang41@gmail.com"},
    {"full_name": "Vũ Thị Xuân", "phone": "0901234042", "address": "Quảng Ninh", "email": "xuan.vu42@gmail.com"},
    {"full_name": "Đặng Văn Yên", "phone": "0901234043", "address": "Bắc Giang", "email": "yen.dang43@gmail.com"},
    {"full_name": "Bùi Thị Anh", "phone": "0901234044", "address": "Hà Nội", "email": "anh.bui44@gmail.com"},
    {"full_name": "Đỗ Văn Bình", "phone": "0901234045", "address": "Hải Dương", "email": "binh.do45@gmail.com"},
    {"full_name": "Hồ Thị Chi", "phone": "0901234046", "address": "Nam Định", "email": "chi.ho46@gmail.com"},
    {"full_name": "Phan Văn Dũng", "phone": "0901234047", "address": "Nghệ An", "email": "dung.phan47@gmail.com"},
    {"full_name": "Lý Thị Hương", "phone": "0901234048", "address": "Hà Nội", "email": "huong.ly48@gmail.com"},
    {"full_name": "Nguyễn Văn Khôi", "phone": "0901234049", "address": "TP.HCM", "email": "khoi.nguyen49@gmail.com"},
    {"full_name": "Trần Thị Lan", "phone": "0901234050", "address": "Đà Nẵng", "email": "lan.tran50@gmail.com"}
]

with app.app_context():
    # Kiểm tra hoặc tạo Admin
    admin_email = "admin@test.com"
    admin = User.query.filter_by(email=admin_email).first()
    
    if not admin:
        try:
            admin_data = register_user(
                email=admin@test.com,
                username="Admin Test",
                password="admin12345"
            )
            admin = User.query.filter_by(email=admin_email).first()
            print(f"Đã tạo tài khoản admin: {admin_email}")
        except Exception as e:
            print(f"❌ Lỗi tạo admin: {e}")
            sys.exit(1)
    else:
        print(f"Tài khoản admin đã tồn tại: {admin_email}")

    # Thêm 50 khách hàng
    added_count = 0
    for contact in contacts:
        try:
            create_customer(user_id=admin.id, data=contact)
            added_count += 1
        except Exception as e:
            print(f"❌ Lỗi thêm KH {contact['full_name']}: {e}")
            
    print(f"\n🎉 Thành công: Đã thêm {added_count} khách hàng mẫu vào tài khoản {admin_email}")
