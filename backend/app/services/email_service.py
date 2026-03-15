import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_email(to_email: str, subject: str, body: str) -> dict:
    try:
        # Load cấu hình SMTP từ app config
        smtp_host = current_app.config.get("SES_SMTP_HOST")
        smtp_port = current_app.config.get("SES_SMTP_PORT", 587)
        smtp_user = current_app.config.get("SES_SMTP_USER")
        smtp_pass = current_app.config.get("SES_SMTP_PASS")
        sender = current_app.config.get("SENDER_EMAIL")

        if not all([smtp_host, smtp_user, smtp_pass]):
            return {
                "success": False,
                "error": "Thiếu cấu hình SMTP trong biến môi trường (.env)"
            }

        # Tạo email message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Kết nối tới SES qua SMTP
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Bật mã hóa TLS
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        return {
            "success": True,
            "message_id": f"smtp-sent-to-{to_email}"
        }

    except Exception as e:
        # Lỗi có thể do: Sai credentials, chưa verify email trên SES (nếu sandbox), ...
        return {
            "success": False,
            "error": f"Lỗi SMTP: {str(e)}"
        }
