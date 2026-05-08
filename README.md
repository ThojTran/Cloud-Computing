# Cloud-Computing: CRM Web Application

Ứng dụng quản lý thông tin khách hàng và hỗ trợ giao tiếp qua SMS và Email trên nền tảng AWS.

## 📋 Tính Năng Chính

- **Quản lý khách hàng** - Thêm, sửa, xóa thông tin khách hàng
- **Xác thực người dùng** - Đăng ký, đăng nhập với JWT
- **Multi-tenant** - Tách biệt dữ liệu theo Organization
- **Gửi SMS** - Tích hợp AWS SNS
- **Gửi Email** - Tích hợp AWS SES
- **Bulk messaging** - Gửi tin nhắn hàng loạt cho nhiều khách hàng

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

## REST API Endpoints
```
Authentication (`/api/auth`)
Customers (`/api/customers`)
Messages (`/api/messages`)
```

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

## 🔗 Truy Cập Ứng Dụng

| Thành phần | URL |
|-----------|-----|
| **Frontend UI** | http://localhost:3000 |
| **Backend API** | http://localhost:5000/api |
| **Production API** | http://54.242.77.45:5000/api |

---

**Created:** Feb 2026  
**Last Updated:** Mar 2026

