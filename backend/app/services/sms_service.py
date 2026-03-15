import boto3
from flask import current_app


def send_sms(phone_number: str, message: str) -> dict:
    """
    Gửi SMS qua AWS SNS.

    Args:
        phone_number: Số điện thoại (format quốc tế, ví dụ: +84912345678)
        message: Nội dung tin nhắn

    Returns:
        dict với 'success' (bool) và 'message_id' hoặc 'error'
    """
    try:
        client = boto3.client(
            "sns",
            region_name=current_app.config["AWS_REGION"],
            aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"],
        )

        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
        )

        return {
            "success": True,
            "message_id": response["MessageId"],
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
