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

#Read All users
@routes_bp.route('/users', methods=['GET'])
def get_users():
    users= User.query.all()
    user_list=[
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_address": user.email_address,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "gender": user.gender,
            "medical_history":user.medical_history,
            "allergies": user.allergies,

        }
        for user in users
    ]
    return jsonify(user_list), 200

#Reading individual users
@routes_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user= User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user_data={
        "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_address": user.email_address,
            "phone_number": user.phone_number,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "gender": user.gender,
            "medical_history":user.medical_history,
            "allergies": user.allergies,
    }
    return jsonify(user_data), 200

#Updating users
@routes_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Get the data from the request
    data = request.get_json()

    try:
        # Update the user fields if provided in the request
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email_address = data.get('email_address', user.email_address)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.gender = data.get('gender', user.gender)
        user.medical_history = data.get('medical_history', user.medical_history)
        user.allergies = data.get('allergies', user.allergies)

        # Commit the changes to the database
        db.session.commit()

        # Return success response
        return jsonify({
            "message": "User updated successfully!",
            "user": {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_address": user.email_address,
                "phone_number": user.phone_number,
                "date_of_birth": user.date_of_birth,
                "gender": user.gender,
                "medical_history": user.medical_history,
                "allergies": user.allergies
            }
        }), 200

    except Exception as e:
        # Rollback any changes in case of an error
        db.session.rollback()
        # Log the error for debugging (optional)
        print(f"Error updating user: {e}")
        return jsonify({"error": str(e)}), 400

# Delete a user
@routes_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
