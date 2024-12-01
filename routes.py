from flask import Blueprint, request, jsonify
from models import db, User  # Import db and User models here

# Create a Blueprint instance
routes_bp = Blueprint('routes', __name__)

# Define CRUD routes for the user table

# Adding a new user
@routes_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email_address=data['email_address'],
            phone_number=data['phone_number'],
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            medical_history=data.get('medical_history'),
            allergies=data.get('allergies')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "User created successfully!",
            "user_id": new_user.user_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
