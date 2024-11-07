from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playbook(db.Model):
    __tablename__ = 'playbooks'
    playbook_id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    response_steps = db.Column(db.Text)
    recovery_steps = db.Column(db.Text)
    continuity_plan = db.Column(db.Text)
    status = db.Column(db.String(50))

class Incident(db.Model):
    __tablename__ = 'incidents'
    incident_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    severity = db.Column(db.Integer)
    status = db.Column(db.String(50))
    detected_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    asset_affected = db.Column(db.String(255))
    description = db.Column(db.Text)
    playbook_id = db.Column(db.Integer, db.ForeignKey('playbooks.playbook_id'))
    recovery_status = db.Column(db.String(50))

class RecoveryAction(db.Model):
    __tablename__ = 'recovery_actions'
    recovery_action_id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.incident_id'))
    action_taken = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50))

class CrisisCommunication(db.Model):
    __tablename__ = 'crisis_communications'
    communication_id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.incident_id'))
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    recipients = db.Column(db.String(255))
    status = db.Column(db.String(50))

class IncidentLog(db.Model):
    __tablename__ = 'incident_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.incident_id'))
    timestamp = db.Column(db.DateTime)
    event_type = db.Column(db.String(100))
    details = db.Column(db.Text)
