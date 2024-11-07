from datetime import datetime

from RITP import db


class Assets(db.Model):
    __tablename__='assets'
    asset_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    type=db.Column(db.String(255),nullable=False)
    value=db.Column(db.Numeric(18, 2)   )
    criticality=db.Column(db.String(50),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    risks = db.relationship('AssetRisk', backref='asset', cascade="all, delete-orphan", lazy=True)

class AssetRisk(db.Model):
    __tablename__ = 'asset_risks'
    risk_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id', ondelete='CASCADE'))
    risk_score = db.Column(db.Numeric(5, 2), nullable=False)
    risk_description = db.Column(db.Text)
    threat_level = db.Column(db.String(20))
    last_evaluation = db.Column(db.DateTime, default=datetime.utcnow)


class Incident(db.Model):
    __tablename__ = 'incidents'

    incident_id = db.Column(db.Integer, primary_key=True)  # Primary Key
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.asset_id', ondelete='CASCADE'),
                         nullable=False)  # Foreign Key referencing 'assets'
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Defaults to current timestamp
    description = db.Column(db.Text, nullable=False)  # Incident description
    impact_score = db.Column(db.Numeric(5, 2), nullable=False)  # Impact score (0-100 range)
    resolved = db.Column(db.Boolean, default=False)  # Resolved status (default is False)
    severity_level = db.Column(db.String(10), nullable=False)  # Severity level (e.g., "High", "Low")
    incident_type = db.Column(db.String(50), nullable=False)  # Type of incident
    duration = db.Column(db.Integer)  # Duration of the incident in minutes