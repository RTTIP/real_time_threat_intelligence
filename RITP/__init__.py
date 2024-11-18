from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nikhilesh@localhost/asset_management_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize the db with the app

    with app.app_context():
        db.create_all()  # Create tables within the app context

    from RITP.routes.crud_operations import crud_bp
    from RITP.routes.predict_impact import predict_bp
    from RITP.routes.read_threat import threat_bp
    from RITP.routes.llm_integration import llm_bp
    from RITP.routes.automated_incident import incident_bp
    from RITP.routes.automated_incident import monitor_risks
    app.register_blueprint(crud_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(threat_bp)
    app.register_blueprint(llm_bp)
    app.register_blueprint(incident_bp)

    def scheduled_task():
        with app.app_context():
            monitor_risks()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_task, trigger="interval", seconds=3)
    scheduler.start()

    return app