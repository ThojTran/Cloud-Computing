# Cloud-Computing: CRM Web Application

Ứng dụng quản lý thông tin khách hàng và hỗ trợ giao tiếp qua SMS và Email trên nền tảng AWS.

## 📋 Tính Năng Chính

- ✅ **Quản lý khách hàng** - Thêm, sửa, xóa thông tin khách hàng
- ✅ **Xác thực người dùng** - Đăng ký, đăng nhập với JWT
- ✅ **Multi-tenant** - Tách biệt dữ liệu theo Organization
- ✅ **Gửi SMS** - Tích hợp AWS SNS
- ✅ **Gửi Email** - Tích hợp AWS SES
- ✅ **Bulk messaging** - Gửi tin nhắn hàng loạt cho nhiều khách hàng

---

## 🏗️ Cấu Trúc Dự Án

```
Cloud-Computing/
├── backend/                    # Flask REST API (Python)
│   ├── app/
│   │   ├── models/            # User, Customer, Message, Organization
│   │   ├── routes/            # API endpoints (auth, customers, messages)
│   │   ├── services/          # Business logic (sms_service, email_service)
│   │   ├── __init__.py        # Flask app factory
│   │   └── config.py          # Configuration
│   ├── migrations/            # Database migrations
│   ├── run.py                 # Entry point
│   └── requirements.txt       # Python dependencies
│
└── frontend/                   # React Web UI
    ├── src/
    │   ├── Auth/              # Login/Register pages
    │   ├── pages/             # Customer, Messages pages
    │   ├── services/          # API calls
    │   ├── App.js             # Main app component
    │   └── config.js          # API endpoint config
    ├── public/                # Static files
    └── package.json           # Dependencies
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy

### **1. Backend (Python Flask)**

#### Yêu cầu
- Python 3.8+
- MySQL Database
- AWS Account (SNS, SES)

#### Các bước cài đặt

```bash
# 1. Vào thư mục backend
cd backend

# 2. Tạo virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Cài đặt dependencies
pip install -r requirements.txt

# 5. Tạo file .env
cp .env.example .env
# Điền các thông tin:
# - SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost:3306/crm_db
# - JWT_SECRET_KEY=your_secret_key
# - AWS_REGION=us-east-1
# - AWS_ACCESS_KEY_ID=your_key
# - AWS_SECRET_ACCESS_KEY=your_secret
# - SES_SMTP_HOST, SES_SMTP_PORT, SES_SMTP_USER, SES_SMTP_PASS
# - SENDER_EMAIL=your_email@example.com

# 6. Tạo database
# mysql -u root -p
# CREATE DATABASE crm_db;

# 7. Chạy migrations
flask db upgrade

# 8. Chạy server
python run.py
```

**Backend chạy tại:** `http://localhost:5000`

---

### **2. Frontend (React)**

#### Yêu cầu
- Node.js 16+
- npm hoặc yarn

#### Các bước cài đặt

```bash
# 1. Vào thư mục frontend
cd frontend

# 2. Cài đặt dependencies
npm install

# 3. Tạo file .env
echo "REACT_APP_BACKEND_URL=http://localhost:5000/api" > .env

# 4. Chạy development server
npm start
```

**Frontend chạy tại:** `http://localhost:3000`

---

## 📡 REST API Endpoints

### **Authentication** (`/api/auth`)
```
POST   /register           - Đăng ký user mới
POST   /login              - Đăng nhập
POST   /register-org       - Tạo org mới + user
POST   /join-org           - Join vào org (cần invite code)
GET    /me                 - Lấy thông tin user hiện tại (cần token)
```

### **Customers** (`/api/customers`)
```
GET    /                   - Lấy danh sách khách hàng
GET    /<id>               - Lấy chi tiết 1 khách hàng
POST   /                   - Thêm khách hàng mới
PUT    /<id>               - Cập nhật khách hàng
DELETE /<id>               - Xóa 1 khách hàng
POST   /bulk-delete        - Xóa nhiều khách hàng
```

### **Messages** (`/api/messages`)
```
POST   /send               - Gửi SMS/Email hàng loạt
GET    /history            - Lấy lịch sử gửi tin
```

---

## 🔐 Xác Thực

Tất cả request (trừ `/register`, `/login`, `/register-org`) cần header:
```
Authorization: Bearer <JWT_TOKEN>
```

**Lấy token:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "password":"password123"}'
```

---

## 🗄️ Database Schema

### Users Table
```sql
- id (PK)
- email (unique)
- username
- password (hashed)
- org_id (FK)
- created_at
```

### Customers Table
```sql
- id (PK)
- org_id (FK)
- full_name
- phone
- email
- address
- created_at
```

### Messages Table
```sql
- id (PK)
- user_id (FK)
- type_ms (sms/email)
- subject
- context_ms
- sent_at
```

### MessageRecipient Table
```sql
- id (PK)
- message_id (FK)
- customer_id (FK)
- status (sent/failed)
```

---

## 🛠️ Công Nghệ Sử Dụng

| Phần | Công Nghệ |
|------|-----------|
| **Backend** | Python, Flask, SQLAlchemy |
| **Database** | MySQL |
| **Frontend** | React, TypeScript, SCSS |
| **Cloud** | AWS (SNS, SES, EC2) |
| **Auth** | JWT (Flask-JWT-Extended) |
| **Deployment** | AWS EC2 |

---

## 📝 Ví Dụ Sử Dụng

### 1. Đăng ký Organization mới
```bash
curl -X POST http://localhost:5000/api/auth/register-org \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Công ty ABC",
    "email": "admin@abc.com",
    "username": "admin",
    "password": "password123"
  }'
```

### 2. Thêm khách hàng
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Nguyễn Văn A",
    "phone": "+84912345678",
    "email": "a@example.com",
    "address": "Hà Nội"
  }'
```

### 3. Gửi SMS cho multiple customers
```bash
curl -X POST http://localhost:5000/api/messages/send \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "sms",
    "subject": null,
    "content": "Xin chào! Đây là thông báo từ công ty",
    "customer_ids": [1, 2, 3]
  }'
```

---

## ⚙️ Biến Môi Trường (.env)

```env
# Database
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost:3306/crm_db

# JWT
JWT_SECRET_KEY=your_secret_key_here

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# AWS SES SMTP
SES_SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SES_SMTP_PORT=587
SES_SMTP_USER=AKIAIOSFODNN7EXAMPLE
SES_SMTP_PASS=BNKjO/Xxxxxxxxxx...
SENDER_EMAIL=noreply@abc.com

# CORS
CORS_ORIGINS=http://localhost:3000

# Frontend
REACT_APP_BACKEND_URL=http://localhost:5000/api
```

---

## 📊 Quy Trình Gửi Tin Nhắn

```
Frontend (React)
    ↓
[POST /api/messages/send]
    ↓
Backend (Flask)
    ├─→ Validate user & organization
    ├─→ Validate customers belong to org
    ├─→ Create Message record
    ├─→ For each customer:
    │   ├─→ Send SMS via AWS SNS (hoặc Email via SES)
    │   └─→ Create MessageRecipient record
    ├─→ Commit to database
    ↓
Response (success/failed status cho từng customer)
```

---

## 🔗 Truy Cập Ứng Dụng

| Thành phần | URL |
|-----------|-----|
| **Frontend UI** | http://localhost:3000 |
| **Backend API** | http://localhost:5000/api |
| **Production API** | http://54.242.77.45:5000/api |

---

## 📞 Liên Hệ & Hỗ Trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra file `.env` đã điền đầy đủ chưa
2. Đảm bảo MySQL và AWS credentials hợp lệ
3. Xem logs từ backend: `python run.py`

---

**Created:** Feb 2026  
**Last Updated:** Mar 2026

