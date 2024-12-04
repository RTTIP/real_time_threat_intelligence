from flask import Flask, request, jsonify
from transformers import pipeline
import logging
import psycopg2 
from app.database import (
    insert_incident, get_incidents, update_incident, delete_incident,
    insert_playbook, get_playbooks, update_playbook, delete_playbook,
    insert_recovery_action, get_recovery_actions, update_recovery_action, delete_recovery_action,
    insert_crisis_communication, get_crisis_communications, update_crisis_communication, delete_crisis_communication,
    insert_incident_log, get_incident_logs, update_incident_log, delete_incident_log,get_related_playbook, get_recovery_actions_for_incident, 
                          get_crisis_communications_for_incident, get_logs_for_incident,
                          update_incident_status,get_incident_by_id,generate_playbook,get_incident_by_id,generate_business_continuity_message
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

# API endpoint for generating messages
@app.route('/generate-business-continuity-message', methods=['POST'])
def generate_message():
    try:
        # Extract data from the request body
        business_continuity_data = request.json
        if not business_continuity_data:
            return jsonify({"error": "No business continuity data provided"}), 400
        
        # Generate message
        generated_message_lines = generate_business_continuity_message(business_continuity_data)
        return jsonify({"message": generated_message_lines})  # Return as a list of lines
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def fetch_incident_data(incident_id):
    """Fetch incident data from the database."""
    try:
        conn = psycopg2.connect(
            host="db-1.c5o4k2em6pvs.us-east-1.rds.amazonaws.com",
            port='5432',
            dbname='postgres',
            user='postgres',
            password='postgres123',
        )
        cur = conn.cursor()
        query = """
        SELECT incident_id, type, asset_affected
        FROM incidents
        WHERE incident_id = %s;
        """
        cur.execute(query, (incident_id,))
        result = cur.fetchone()
        if result:
            incident_data = {
                "incident_id": result[0],
                "incident_type": result[1],
                "affected_systems": result[2].split(",")  # Assuming `asset_affected` is a comma-separated string
            }
            return incident_data
        else:
            logging.info(f"No data found for Incident ID {incident_id}.")
            return None
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None
    finally:
        if conn:
            conn.close()



# Generate Incident Prompts 
# Initialize logging
logging.basicConfig(level=logging.INFO)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # Use CPU


def generate_prompt_with_incident_data(incident_data):
    """Generate the prompt for the summarizer."""
    return f"""
    type: {incident_data['incident_type']}
    asset_affected: {', '.join(incident_data['affected_systems'])}

    Provide a concise summary of the incident type and its impact on the affected assets.
    Include recommendations for mitigating any potential issues and restoring operations.
    """


def summarize_incident(incident_data):
    """Generate a summary based on the incident data."""
    prompt = generate_prompt_with_incident_data(incident_data)
    try:
        summary = summarizer(prompt, max_length=200, min_length=80, do_sample=True, top_k=50, temperature=0.9)
        logging.info(f"Generated summary: {summary[0]['summary_text']}")
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return f"Error generating summary: {str(e)}"


@app.route('/api/incidents/generate-summary', methods=['POST'])
def generate_incident_summary():
    """API endpoint to generate an incident summary."""
    try:
        # Extract data from request
        data = request.json
        incident_id = data.get('incident_id')
        
        if not incident_id:
            return jsonify({
                "status": "error",
                "message": "Incident ID is required."
            }), 400
        
        logging.info(f"Fetching data for incident ID: {incident_id}")
        incident_data = fetch_incident_data(incident_id)

        if incident_data:
            logging.info(f"Fetched Incident Data: {incident_data}")
            summary = summarize_incident(incident_data)
            return jsonify({
                "status": "success",
                "message": "Summary generated successfully.",
                "data": {
                    "incident_id": incident_data['incident_id'],
                    "summary": summary
                }
            }), 200
        else:
            logging.error(f"Incident data not found for ID: {incident_id}")
            return jsonify({
                "status": "error",
                "message": "Incident data not found."
            }), 404

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while processing the request. Please try again later."
        }), 500

#Generate Playbook prompts

# Initialize the summarizer with explicit device configuration
# Initialize logging
logging.basicConfig(level=logging.INFO)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # Use CPU


def fetch_playbook_data(incident_id):
    """Fetch incident data along with continuity plan and impact summary from the database."""
    try:
        conn = psycopg2.connect(
            host="db-1.c5o4k2em6pvs.us-east-1.rds.amazonaws.com",
            port='5432',
            dbname='postgres',
            user='postgres',
            password='postgres123',
        )
        cur = conn.cursor()
        query = """
        SELECT p.incident_id, p.continuity_plan, i.details
        FROM playbooks p
        JOIN incident_logs i
        ON i.incident_id = p.incident_id
        WHERE p.incident_id = %s;
        """
        cur.execute(query, (incident_id,))
        result = cur.fetchone()
        if result:
            incident_data = {
                "incident_id": result[0],
                "continuity_plan": result[1],
                "impact_summary": result[2],  # Renamed from incident_details
            }
            return incident_data
        else:
            logging.info(f"No data found for Incident ID {incident_id}.")
            return None
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        return None
    finally:
        if conn:
            conn.close()


def generate_prompt_with_plan(incident_data):
    """Generate the prompt for the summarizer with continuity plan and impact summary."""
    return f"""
    Incident ID: {incident_data['incident_id']}
    Business Continuity Plan: {incident_data['continuity_plan']}
    Impact Summary: {incident_data['impact_summary']}

    Generate a message for all employees and key stakeholders, explaining the incident's impact on business operations, the measures in place to ensure continuity, and any changes or instructions they should follow.
    """


def summarize_incident_with_plan(incident_data):
    """Generate a summary based on the incident data."""
    prompt = generate_prompt_with_plan(incident_data)
    try:
        summary = summarizer(prompt, max_length=250, min_length=120, do_sample=True, top_k=50, temperature=0.9)
        logging.info(f"Generated summary: {summary[0]['summary_text']}")
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return f"Error generating summary: {str(e)}"


@app.route('/api/crisis-management/generate-stakeholder-message', methods=['POST'])
def generate_stakeholder_message():
    """API endpoint to generate stakeholder communication message."""
    try:
        # Extract data from request
        data = request.json
        incident_id = data.get('incident_id')
        
        if not incident_id:
            return jsonify({
                "status": "error",
                "message": "Incident ID is required."
            }), 400
        
        logging.info(f"Fetching data for incident ID: {incident_id}")
        incident_data = fetch_playbook_data(incident_id)

        if incident_data:
            logging.info(f"Fetched Incident Data: {incident_data}")
            summary = summarize_incident_with_plan(incident_data)
            return jsonify({
                "status": "success",
                "message": "Message generated and processed successfully.",
                "data": {
                    "incident_id": incident_data['incident_id'],
                    "summary": summary
                }
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Incident data not found."
            }), 404

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while processing the request. Please try again later."
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)