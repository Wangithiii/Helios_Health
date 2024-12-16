from flask import Blueprint, request, jsonify
from models import db, Specialist

# Create a Blueprint for specialist routes
specialist_routes = Blueprint('specialist_routes', __name__)

# Create a new specialist
@specialist_routes.route('/specialists', methods=['POST'])
def create_specialist():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request payload is required"}), 400

    try:
        new_specialist = Specialist(
            specialty=data['specialty'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email_address=data['email_address'],
            available_times=data.get('available_times')
        )
        db.session.add(new_specialist)
        db.session.commit()
        return jsonify({"message": "Specialist created successfully!", "specialist_id": new_specialist.specialist_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Read all specialists
@specialist_routes.route('/specialists', methods=['GET'])
def get_all_specialists():
    specialists = Specialist.query.all()
    return jsonify([{
        "specialist_id": specialist.specialist_id,
        "specialty": specialist.specialty,
        "first_name": specialist.first_name,
        "last_name": specialist.last_name,
        "phone_number": specialist.phone_number,
        "email_address": specialist.email_address,
        "available_times": specialist.available_times
    } for specialist in specialists]), 200

# Read a specialist by ID
@specialist_routes.route('/specialists/<int:specialist_id>', methods=['GET'])
def get_specialist_by_id(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if not specialist:
        return jsonify({"error": "Specialist not found"}), 404

    return jsonify({
        "specialist_id": specialist.specialist_id,
        "specialty": specialist.specialty,
        "first_name": specialist.first_name,
        "last_name": specialist.last_name,
        "phone_number": specialist.phone_number,
        "email_address": specialist.email_address,
        "available_times": specialist.available_times
    }), 200

# Update a specialist by ID
@specialist_routes.route('/specialists/<int:specialist_id>', methods=['PUT'])
def update_specialist(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if not specialist:
        return jsonify({"error": "Specialist not found"}), 404

    data = request.get_json()
    try:
        specialist.specialty = data.get('specialty', specialist.specialty)
        specialist.first_name = data.get('first_name', specialist.first_name)
        specialist.last_name = data.get('last_name', specialist.last_name)
        specialist.phone_number = data.get('phone_number', specialist.phone_number)
        specialist.email_address = data.get('email_address', specialist.email_address)
        specialist.available_times = data.get('available_times', specialist.available_times)

        db.session.commit()
        return jsonify({"message": "Specialist updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Delete a specialist by ID
@specialist_routes.route('/specialists/<int:specialist_id>', methods=['DELETE'])
def delete_specialist(specialist_id):
    specialist = Specialist.query.get(specialist_id)
    if not specialist:
        return jsonify({"error": "Specialist not found"}), 404

    try:
        db.session.delete(specialist)
        db.session.commit()
        return jsonify({"message": "Specialist deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
