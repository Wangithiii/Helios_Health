from flask import Blueprint, request, jsonify
from models import db, Medication

# Create a Blueprint instance for medication routes
medication_routes = Blueprint('medication_routes', __name__)

# Create a new medication entry
@medication_routes.route('/medications', methods=['POST'])
def create_medication():
    data = request.get_json()
    try:
        new_medication = Medication(
            user_id=data['user_id'],
            medication_name=data['medication_name'],
            dosage=data['dosage'],
            frequency=data['frequency'],
            start_date=data['start_date'],
            end_date=data.get('end_date'),
            notes=data.get('notes')
        )
        db.session.add(new_medication)
        db.session.commit()
        return jsonify({
            "message": "Medication created successfully!",
            "medication_id": new_medication.medication_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Read all 
@medication_routes.route('/medications', methods=['GET'])
def get_all_medications():
    medications = Medication.query.all()
    return jsonify([{
        "medication_id": med.medication_id,
        "user_id": med.user_id,
        "medication_name": med.medication_name,
        "dosage": med.dosage,
        "frequency": med.frequency,
        "start_date": med.start_date,
        "end_date": med.end_date,
        "notes": med.notes
    } for med in medications]), 200

# Read a single medication by ID
@medication_routes.route('/medications/<int:medication_id>', methods=['GET'])
def get_medication_by_id(medication_id):
    medication = Medication.query.get(medication_id)
    if medication is None:
        return jsonify({"error": "Medication not found"}), 404
    return jsonify({
        "medication_id": medication.medication_id,
        "user_id": medication.user_id,
        "medication_name": medication.medication_name,
        "dosage": medication.dosage,
        "frequency": medication.frequency,
        "start_date": medication.start_date,
        "end_date": medication.end_date,
        "notes": medication.notes
    }), 200

# Update a medication by ID
@medication_routes.route('/medications/<int:medication_id>', methods=['PUT'])
def update_medication(medication_id):
    medication = Medication.query.get(medication_id)
    if medication is None:
        return jsonify({"error": "Medication not found"}), 404
    
    data = request.get_json()
    try:
        medication.medication_name = data.get('medication_name', medication.medication_name)
        medication.dosage = data.get('dosage', medication.dosage)
        medication.frequency = data.get('frequency', medication.frequency)
        medication.start_date = data.get('start_date', medication.start_date)
        medication.end_date = data.get('end_date', medication.end_date)
        medication.notes = data.get('notes', medication.notes)
        
        db.session.commit()
        return jsonify({"message": "Medication updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Delete a medication by ID
@medication_routes.route('/medications/<int:medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    medication = Medication.query.get(medication_id)
    if medication is None:
        return jsonify({"error": "Medication not found"}), 404
    
    try:
        db.session.delete(medication)
        db.session.commit()
        return jsonify({"message": "Medication deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
