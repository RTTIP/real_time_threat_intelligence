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

