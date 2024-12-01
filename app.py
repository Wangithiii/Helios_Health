from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Import and register routes
from routes import routes_bp
app.register_blueprint(routes_bp)

# Basic home route
@app.route('/')
def home():
    return "Hello, Flask with SQLAlchemy!"

# This ensures the app runs if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)
