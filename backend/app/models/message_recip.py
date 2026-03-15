from app.extensions import db
from datetime import datetime, timezone


class MessageRecipient(db.Model):
    __tablename__ = "MESSAGES_RECIPIENTS"

    id          = db.Column("ID", db.Integer, primary_key=True)
    message_id  = db.Column("MESSAGE_ID", db.Integer,
                            db.ForeignKey("MESSAGES.ID"), nullable=False)
    customer_id = db.Column("CUSTOMER_ID", db.Integer,
                            db.ForeignKey("CUSTOMERS.ID"), nullable=False)
    status      = db.Column("STATUS", db.String(20), nullable=False,
                            default="pending")  # 'pending' | 'sent' | 'failed'
    sent_at     = db.Column("SENT_AT", db.DateTime,
                            default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "message_id": self.message_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer.full_name if self.customer else None,
            "status": self.status,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }