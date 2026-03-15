from app.extensions import db
from datetime import datetime, timezone


class Message(db.Model):
    __tablename__ = "MESSAGES"

    id         = db.Column("ID", db.Integer, primary_key=True)
    user_id    = db.Column("USER_ID", db.Integer,
                           db.ForeignKey("users.id"), nullable=False)  # Ai đã gửi message
    type_ms    = db.Column("TYPE_MS", db.String(10), nullable=False)   # 'sms' | 'email'
    subject    = db.Column("SUBJECT", db.String(200))                  # Subject cho email (SMS thì null)
    context_ms = db.Column("CONTEXT_MS", db.Text, nullable=False)      # Nội dung message
    sent_at    = db.Column("SENT_AT", db.DateTime,
                           default=lambda: datetime.now(timezone.utc))

    # 1 message gửi cho nhiều recipients
    recipients = db.relationship("MessageRecipient", backref="message", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type_ms,
            "subject": self.subject,
            "content": self.context_ms,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "recipients": [r.to_dict() for r in self.recipients],
        }
