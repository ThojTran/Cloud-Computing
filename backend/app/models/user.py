from app.extensions import db
from datetime import datetime, timezone
import bcrypt


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(100), unique=True, nullable=False)
    username      = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # 255 cho bcrypt hash
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships – 1 user có nhiều customers và nhiều messages
    customers = db.relationship("Customer", backref="owner", lazy=True)
    messages  = db.relationship("Message",  backref="sender", lazy=True)

    # --------------- Password helpers ---------------
    def set_password(self, raw: str):
        self.password_hash = bcrypt.hashpw(
            raw.encode(), bcrypt.gensalt()
        ).decode()

    def check_password(self, raw: str) -> bool:
        return bcrypt.checkpw(raw.encode(), self.password_hash.encode())

    # --------------- Serialization ---------------
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }