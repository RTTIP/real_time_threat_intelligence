from flask import Blueprint, jsonify
from .models import Playbook, Incident, RecoveryAction, CrisisCommunication, IncidentLog

bp = Blueprint('main', __name__)

@bp.route('/playbooks', methods=['GET'])
def get_playbooks():
    playbooks = Playbook.query.all()
    return jsonify([{
        'playbook_id': p.playbook_id,
        'incident_id': p.incident_id,
        'created_at': p.created_at,
        'response_steps': p.response_steps,
        'recovery_steps': p.recovery_steps,
        'continuity_plan': p.continuity_plan,
        'status': p.status
    } for p in playbooks])

@bp.route('/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([{
        'incident_id': i.incident_id,
        'type': i.type,
        'severity': i.severity,
        'status': i.status,
        'detected_at': i.detected_at,
        'resolved_at': i.resolved_at,
        'asset_affected': i.asset_affected,
        'description': i.description,
        'playbook_id': i.playbook_id,
        'recovery_status': i.recovery_status
    } for i in incidents])

@bp.route('/recovery_actions', methods=['GET'])
def get_recovery_actions():
    actions = RecoveryAction.query.all()
    return jsonify([{
        'recovery_action_id': a.recovery_action_id,
        'incident_id': a.incident_id,
        'action_taken': a.action_taken,
        'started_at': a.started_at,
        'completed_at': a.completed_at,
        'status': a.status
    } for a in actions])

@bp.route('/crisis_communications', methods=['GET'])
def get_crisis_communications():
    communications = CrisisCommunication.query.all()
    return jsonify([{
        'communication_id': c.communication_id,
        'incident_id': c.incident_id,
        'message': c.message,
        'sent_at': c.sent_at,
        'recipients': c.recipients,
        'status': c.status
    } for c in communications])

@bp.route('/incident_logs', methods=['GET'])
def get_incident_logs():
    logs = IncidentLog.query.all()
    return jsonify([{
        'log_id': l.log_id,
        'incident_id': l.incident_id,
        'timestamp': l.timestamp,
        'event_type': l.event_type,
        'details': l.details
    } for l in logs])
