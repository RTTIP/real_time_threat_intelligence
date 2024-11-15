from flask import Flask, request, jsonify
from app.database import (
    insert_incident, get_incidents, update_incident, delete_incident,
    insert_playbook, get_playbooks, update_playbook, delete_playbook,
    insert_recovery_action, get_recovery_actions, update_recovery_action, delete_recovery_action,
    insert_crisis_communication, get_crisis_communications, update_crisis_communication, delete_crisis_communication,
    insert_incident_log, get_incident_logs, update_incident_log, delete_incident_log,get_related_playbook, get_recovery_actions_for_incident, 
                          get_crisis_communications_for_incident, get_logs_for_incident,
                          update_incident_status,get_incident_by_id,generate_playbook,get_incident_by_id
)

app = Flask(__name__)

# Default route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Threat Intelligence Platform API"}), 200

# -------------------- INCIDENTS --------------------#

@app.route('/api/incidents', methods=['POST'])
def add_incident():
    data = request.get_json()
    try:
        insert_incident(data)
        return jsonify({"message": "Incident added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/incidents', methods=['GET'])
def get_all_incidents():
    try:
        incidents = get_incidents()
        return jsonify(incidents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/incidents/<int:incident_id>', methods=['GET'])
def get_specific_incident(incident_id):
    """
    API endpoint to get a specific incident by its ID.
    """
    incident = get_incident_by_id(incident_id)
    if incident:
        return jsonify(incident), 200
    else:
        return jsonify({"error": "Incident not found"}), 404

@app.route('/api/incidents/<int:id>', methods=['PUT'])
def modify_incident(id):
    data = request.get_json()
    try:
        update_incident(id, data)
        return jsonify({"message": "Incident updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/incidents/<int:id>', methods=['DELETE'])
def remove_incident(id):
    try:
        delete_incident(id)
        return jsonify({"message": "Incident deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- PLAYBOOKS --------------------

@app.route('/api/playbooks', methods=['POST'])
def add_playbook():
    data = request.get_json()
    try:
        playbook_id = insert_playbook(data)
        return jsonify({"message": "Playbook added successfully!", "playbook_id": playbook_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/playbooks', methods=['GET'])
def get_all_playbooks():
    try:
        playbooks = get_playbooks()
        return jsonify(playbooks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/playbooks/<int:id>', methods=['PUT'])
def modify_playbook(id):
    data = request.get_json()
    try:
        update_playbook(id, data)
        return jsonify({"message": "Playbook updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/playbooks/<int:id>', methods=['DELETE'])
def remove_playbook(id):
    try:
        delete_playbook(id)
        return jsonify({"message": "Playbook deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- RECOVERY ACTIONS --------------------

@app.route('/api/recovery_actions', methods=['POST'])
def add_recovery_action():
    data = request.get_json()
    try:
        insert_recovery_action(data)
        return jsonify({"message": "Recovery action added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recovery_actions', methods=['GET'])
def get_all_recovery_actions():
    try:
        actions = get_recovery_actions()
        return jsonify(actions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recovery_actions/<int:id>', methods=['PUT'])
def modify_recovery_action(id):
    data = request.get_json()
    try:
        update_recovery_action(id, data)
        return jsonify({"message": "Recovery action updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recovery_actions/<int:id>', methods=['DELETE'])
def remove_recovery_action(id):
    try:
        delete_recovery_action(id)
        return jsonify({"message": "Recovery action deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- CRISIS COMMUNICATIONS --------------------

@app.route('/api/crisis_communications', methods=['POST'])
def add_crisis_communication():
    data = request.get_json()
    try:
        insert_crisis_communication(data)
        return jsonify({"message": "Crisis communication added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crisis_communications', methods=['GET'])
def get_all_crisis_communications():
    try:
        communications = get_crisis_communications()
        return jsonify(communications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crisis_communications/<int:id>', methods=['PUT'])
def modify_crisis_communication(id):
    data = request.get_json()
    try:
        update_crisis_communication(id, data)
        return jsonify({"message": "Crisis communication updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crisis_communications/<int:id>', methods=['DELETE'])
def remove_crisis_communication(id):
    try:
        delete_crisis_communication(id)
        return jsonify({"message": "Crisis communication deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- INCIDENT LOGS --------------------

@app.route('/api/incident_logs', methods=['POST'])
def add_incident_log():
    data = request.get_json()
    try:
        insert_incident_log(data)
        return jsonify({"message": "Incident log added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/incident_logs', methods=['GET'])
def get_all_incident_logs():
    try:
        logs = get_incident_logs()
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/incident_logs/<int:id>', methods=['PUT'])
def modify_incident_log(id):
    data = request.get_json()
    try:
        update_incident_log(id, data)
        return jsonify({"message": "Incident log updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/incident_logs/<int:id>', methods=['DELETE'])
def remove_incident_log(id):
    try:
        delete_incident_log(id)
        return jsonify({"message": "Incident log deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

#-----------------------------------------------------------------------#

# Endpoint to get an incident with related data
@app.route('/api/incidents/<int:incident_id>/details', methods=['GET'])
def get_incident_details(incident_id):
    try:
        # Retrieve data associated with the incident
        playbook = get_related_playbook(incident_id)
        recovery_actions = get_recovery_actions_for_incident(incident_id)
        crisis_communications = get_crisis_communications_for_incident(incident_id)
        logs = get_logs_for_incident(incident_id)
        
        return jsonify({
            "incident_id": incident_id,
            "playbook": playbook,
            "recovery_actions": recovery_actions,
            "crisis_communications": crisis_communications,
            "logs": logs
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to update incident status
@app.route('/api/incidents/<int:incident_id>/status', methods=['PUT'])
def modify_incident_status(incident_id):
    data = request.get_json()
    new_status = data.get("status")
    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    try:
        update_incident_status(incident_id, new_status)
        return jsonify({"message": "Incident status updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# endpoint to generate and retrieve a playbook for a given incident ID.

@app.route('/api/incidents/<int:incident_id>/playbook', methods=['GET'])
def get_incident_playbook(incident_id):
    incident = get_incident_by_id(incident_id)  # Assuming you have a function to fetch a single incident
    if incident is None:
        return jsonify({"error": "Incident not found"}), 404

    playbook = generate_playbook(incident)
    return jsonify({"playbook": playbook}), 200

#To manage the business continuity and recovery for an incident
# endpoint that updates the incident status to "Resolved" if it's not already resolved.

@app.route('/api/incidents/<int:incident_id>/recover', methods=['POST'])
def recover_incident(incident_id):
    incident = get_incident_by_id(incident_id)  # Assuming you have a function to fetch a single incident
    if incident is None:
        return jsonify({"error": "Incident not found"}), 404

    if incident['status'] != 'Resolved':
        # Update incident status to 'Resolved' and save changes
        update_incident_status(incident_id, 'Resolved')  # Assuming you already have this function
        return jsonify({"message": "Incident recovered successfully."}), 200

    return jsonify({"message": "Incident is already resolved."}), 200




