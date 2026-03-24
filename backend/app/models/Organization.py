from app.extensions import db
from datetime import datetime, timezone

# app/models/organization.py
class Organization(db.Model):
    __tablename__ = "organizations"
    
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    invite_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # 1 org có nhiều users và nhiều customers
    users     = db.relationship("User", backref="organization", lazy=True)
    customers = db.relationship("Customer", backref="organization", lazy=True)