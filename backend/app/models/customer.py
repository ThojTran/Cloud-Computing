from app.extensions import db
from datetime import datetime, timezone


class Customer(db.Model):
    __tablename__ = "CUSTOMERS"

    id         = db.Column("ID", db.Integer, primary_key=True)
    user_id    = db.Column("USER_ID", db.Integer,
                           db.ForeignKey("users.id"), nullable=False)  # Mỗi customer thuộc về 1 user
    full_name  = db.Column("FULL_NAME", db.String(75), nullable=False)
    address    = db.Column("ADDRESS", db.String(100))
    phone      = db.Column("PHONE", db.String(30))
    email      = db.Column("EMAIL", db.String(100))
    created_at = db.Column("CREATED_AT", db.DateTime,
                           default=lambda: datetime.now(timezone.utc))

    # 1 customer có thể nhận nhiều messages
    received_messages = db.relationship(
        "MessageRecipient", backref="customer", lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }