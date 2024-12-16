from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from extensions import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Import and register routes
from user_routes import routes_bp
app.register_blueprint(routes_bp)
from health_log_routes import health_log_routes
app.register_blueprint(health_log_routes)
from medication_routes import medication_routes
app.register_blueprint(medication_routes)
from chronicc_conditions_routes import chronic_condition_routes
app.register_blueprint(chronic_condition_routes)
from specialist_routes import specialist_routes
app.register_blueprint(specialist_routes)


# Basic home route
@app.route('/')
def home():
    return "Hello, Flask with SQLAlchemy!"

# This ensures the app runs if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
