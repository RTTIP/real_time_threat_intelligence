# app/database.py

import psycopg2
from app.config import DB_CONFIG
from psycopg2 import sql

def get_db_connection():
    """
    Establishes and returns a new database connection.
    """
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )
    return conn

def fetch_all(cursor):
    """
    Helper function to fetch all rows and convert them to a list of dictionaries.
    """
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# -------------------- INCIDENTS --------------------

def insert_incident(data):
    """
    Inserts a new incident into the incidents table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO incidents 
    (type, severity, status, detected_at, resolved_at, asset_affected, playbook_id, recovery_status, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING incident_id;
    """
    cursor.execute(query, [
        data["type"],
        data["severity"],
        data["status"],
        data.get("detected_at"),
        data.get("resolved_at"),
        data.get("asset_affected"),
        data.get("playbook_id"),
        data.get("recovery_status"),
        data.get("description")
    ])
    incident_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return incident_id

def get_incidents():
    """
    Retrieves all incidents from the incidents table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents;")
    incidents = fetch_all(cursor)
    cursor.close()
    conn.close()
    return incidents

def get_incident_by_id(incident_id):
    """
    Retrieves a single incident by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE incident_id = %s;", (incident_id,))
    incident = cursor.fetchone()
    cursor.close()
    conn.close()
    if incident:
        return dict(zip([desc[0] for desc in cursor.description], incident))
    return None

def update_incident(incident_id, data):
    """
    Updates an existing incident.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE incidents
    SET type = %s,
        severity = %s,
        status = %s,
        detected_at = %s,
        resolved_at = %s,
        asset_affected = %s,
        playbook_id = %s,
        recovery_status = %s,
        description = %s
    WHERE incident_id = %s;
    """
    cursor.execute(query, [
        data.get("type"),
        data.get("severity"),
        data.get("status"),
        data.get("detected_at"),
        data.get("resolved_at"),
        data.get("asset_affected"),
        data.get("playbook_id"),
        data.get("recovery_status"),
        data.get("description"),
        incident_id
    ])
    conn.commit()
    cursor.close()
    conn.close()

def delete_incident(incident_id):
    """
    Deletes an incident by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidents WHERE incident_id = %s;", (incident_id,))
    conn.commit()
    cursor.close()
    conn.close()

# -------------------- PLAYBOOKS --------------------

def insert_playbook(data):
    """
    Inserts a new playbook into the playbooks table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO playbooks 
    (incident_id, created_at, response_steps, recovery_steps, continuity_plan, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING playbook_id;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("created_at"),
        data.get("response_steps"),
        data.get("recovery_steps"),
        data.get("continuity_plan"),
        data.get("status")
    ])
    playbook_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return playbook_id

def get_playbooks():
    """
    Retrieves all playbooks from the playbooks table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playbooks;")
    playbooks = fetch_all(cursor)
    cursor.close()
    conn.close()
    return playbooks

def get_playbook_by_id(playbook_id):
    """
    Retrieves a single playbook by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playbooks WHERE playbook_id = %s;", (playbook_id,))
    playbook = cursor.fetchone()
    cursor.close()
    conn.close()
    if playbook:
        return dict(zip([desc[0] for desc in cursor.description], playbook))
    return None

def update_playbook(playbook_id, data):
    """
    Updates an existing playbook.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE playbooks
    SET incident_id = %s,
        created_at = %s,
        response_steps = %s,
        recovery_steps = %s,
        continuity_plan = %s,
        status = %s
    WHERE playbook_id = %s;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("created_at"),
        data.get("response_steps"),
        data.get("recovery_steps"),
        data.get("continuity_plan"),
        data.get("status"),
        playbook_id
    ])
    conn.commit()
    cursor.close()
    conn.close()

def delete_playbook(playbook_id):
    """
    Deletes a playbook by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM playbooks WHERE playbook_id = %s;", (playbook_id,))
    conn.commit()
    cursor.close()
    conn.close()

# -------------------- RECOVERY ACTIONS --------------------

def insert_recovery_action(data):
    """
    Inserts a new recovery action into the recovery_actions table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO recovery_actions 
    (incident_id, action_taken, started_at, completed_at, status)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING recovery_action_id;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("action_taken"),
        data.get("started_at"),
        data.get("completed_at"),
        data.get("status")
    ])
    recovery_action_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return recovery_action_id

def get_recovery_actions():
    """
    Retrieves all recovery actions from the recovery_actions table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recovery_actions;")
    actions = fetch_all(cursor)
    cursor.close()
    conn.close()
    return actions

def get_recovery_action_by_id(recovery_action_id):
    """
    Retrieves a single recovery action by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recovery_actions WHERE recovery_action_id = %s;", (recovery_action_id,))
    action = cursor.fetchone()
    cursor.close()
    conn.close()
    if action:
        return dict(zip([desc[0] for desc in cursor.description], action))
    return None

def update_recovery_action(recovery_action_id, data):
    """
    Updates an existing recovery action.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE recovery_actions
    SET incident_id = %s,
        action_taken = %s,
        started_at = %s,
        completed_at = %s,
        status = %s
    WHERE recovery_action_id = %s;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("action_taken"),
        data.get("started_at"),
        data.get("completed_at"),
        data.get("status"),
        recovery_action_id
    ])
    conn.commit()
    cursor.close()
    conn.close()

def delete_recovery_action(recovery_action_id):
    """
    Deletes a recovery action by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recovery_actions WHERE recovery_action_id = %s;", (recovery_action_id,))
    conn.commit()
    cursor.close()
    conn.close()

# -------------------- CRISIS COMMUNICATIONS --------------------

def insert_crisis_communication(data):
    """
    Inserts a new crisis communication into the crisis_communications table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO crisis_communications 
    (incident_id, message, sent_at, recipients, status)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING communication_id;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("message"),
        data.get("sent_at"),
        data.get("recipients"),
        data.get("status")
    ])
    communication_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return communication_id

def get_crisis_communications():
    """
    Retrieves all crisis communications from the crisis_communications table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crisis_communications;")
    communications = fetch_all(cursor)
    cursor.close()
    conn.close()
    return communications

def get_crisis_communication_by_id(communication_id):
    """
    Retrieves a single crisis communication by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crisis_communications WHERE communication_id = %s;", (communication_id,))
    communication = cursor.fetchone()
    cursor.close()
    conn.close()
    if communication:
        return dict(zip([desc[0] for desc in cursor.description], communication))
    return None

def update_crisis_communication(communication_id, data):
    """
    Updates an existing crisis communication.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE crisis_communications
    SET incident_id = %s,
        message = %s,
        sent_at = %s,
        recipients = %s,
        status = %s
    WHERE communication_id = %s;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("message"),
        data.get("sent_at"),
        data.get("recipients"),
        data.get("status"),
        communication_id
    ])
    conn.commit()
    cursor.close()
    conn.close()

def delete_crisis_communication(communication_id):
    """
    Deletes a crisis communication by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM crisis_communications WHERE communication_id = %s;", (communication_id,))
    conn.commit()
    cursor.close()
    conn.close()

# -------------------- INCIDENT LOGS --------------------

def insert_incident_log(data):
    """
    Inserts a new incident log into the incident_logs table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO incident_logs 
    (incident_id, timestamp, event_type, details)
    VALUES (%s, %s, %s, %s)
    RETURNING log_id;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("timestamp"),
        data.get("event_type"),
        data.get("details")
    ])
    log_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return log_id

def get_incident_logs():
    """
    Retrieves all incident logs from the incident_logs table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incident_logs;")
    logs = fetch_all(cursor)
    cursor.close()
    conn.close()
    return logs

def get_incident_log_by_id(log_id):
    """
    Retrieves a single incident log by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incident_logs WHERE log_id = %s;", (log_id,))
    log = cursor.fetchone()
    cursor.close()
    conn.close()
    if log:
        return dict(zip([desc[0] for desc in cursor.description], log))
    return None

def update_incident_log(log_id, data):
    """
    Updates an existing incident log.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE incident_logs
    SET incident_id = %s,
        timestamp = %s,
        event_type = %s,
        details = %s
    WHERE log_id = %s;
    """
    cursor.execute(query, [
        data.get("incident_id"),
        data.get("timestamp"),
        data.get("event_type"),
        data.get("details"),
        log_id
    ])
    conn.commit()
    cursor.close()
    conn.close()

def delete_incident_log(log_id):
    """
    Deletes an incident log by its ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incident_logs WHERE log_id = %s;", (log_id,))
    conn.commit()
    cursor.close()
    conn.close()



# --------Functions that Retrieve associated playbooks, recovery_actions, crisis_communications, and incident_logs for a given incident. --------------------

def get_related_playbook(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playbooks WHERE incident_id = %s", (incident_id,))
    playbook = cursor.fetchone()
    cursor.close()
    conn.close()
    return playbook

def get_recovery_actions_for_incident(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recovery_actions WHERE incident_id = %s", (incident_id,))
    actions = cursor.fetchall()
    cursor.close()
    conn.close()
    return actions

def get_crisis_communications_for_incident(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crisis_communications WHERE incident_id = %s", (incident_id,))
    communications = cursor.fetchall()
    cursor.close()
    conn.close()
    return communications

def get_logs_for_incident(incident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incident_logs WHERE incident_id = %s", (incident_id,))
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs

def update_incident_status(incident_id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status = %s WHERE incident_id = %s", (new_status, incident_id))
    conn.commit()
    cursor.close()
    conn.close()
    

#-----------------------------------------
# generate_playbook function to create a response based on incident details. 

def generate_playbook(incident):
    """
    Generates a simple playbook based on the incident's description and severity.
    Modify this function as needed to provide a more detailed response.
    """
    playbook = (
        f"Playbook for Incident:\n"
        f"Description: {incident['description']}\n"
        f"Severity Level: {incident['severity']}\n\n"
        f"Steps:\n"
        f"1. Assess the incident severity level.\n"
        f"2. Gather initial incident details and logs.\n"
        f"3. Notify relevant stakeholders based on severity.\n"
        f"4. Initiate containment measures.\n"
        f"5. Begin root cause analysis and initiate corrective actions.\n"
        f"6. Monitor the situation until fully resolved.\n"
    )
    return playbook

# Mock generator function for demonstration
def generator(prompt, max_length=100, num_return_sequences=1, truncation=True, no_repeat_ngram_size=2, pad_token_id=50256):
    # Simulated AI response for testing
    return [{"generated_text": f"Generated Message:\n    Incident ID: 12345\n    Business Continuity Plan: Ensure operational capacity through backup systems.\n    Impact Summary: Service disruption for 2 hours.\n    Generate a message for all employees and key stakeholders, explaining the incident's impact on business operations, the measures in place to ensure continuity, and any adjustments required.\n"}]

# Function to generate the business continuity message
def generate_business_continuity_message(business_continuity_data):
    prompt = f"""
    Incident ID: {business_continuity_data['incident_id']}
    Business Continuity Plan: {business_continuity_data['continuity_plan']}
    Impact Summary: {business_continuity_data['impact_summary']}
    
    Generate a message for all employees and key stakeholders, explaining the incident's impact on business operations, the measures in place to ensure continuity, and any adjustments required.
    """
    response = generator(prompt, max_length=100, num_return_sequences=1, truncation=True, no_repeat_ngram_size=2, pad_token_id=50256)
    # Split the generated message by newlines and remove empty lines
    message_lines = response[0]["generated_text"].split("\n")
    clean_lines = [line.strip() for line in message_lines if line.strip()]  # Remove empty and extra spaces
    return clean_lines


