from flask import Blueprint, request, jsonify
from models import db, ChronicCondition

# Create a Blueprint instance
chronic_condition_routes = Blueprint('chronic_condition_routes', __name__)

# Create a new chronic condition entry
@chronic_condition_routes.route('/chronic_conditions', methods=['POST'])
def create_chronic_condition():
    data = request.get_json()
    try:
        new_condition = ChronicCondition(
            user_id=data['user_id'],
            condition_name=data['condition_name'],
            diagnosis_date=data.get('diagnosis_date'),
            current_status=data.get('current_status')
        )
        db.session.add(new_condition)
        db.session.commit()
        return jsonify({
            "message": "Chronic condition created successfully!",
            "condition_id": new_condition.condition_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Read all chronic conditions
@chronic_condition_routes.route('/chronic_conditions', methods=['GET'])
def get_all_chronic_conditions():
    conditions = ChronicCondition.query.all()
    return jsonify([{
        "condition_id": condition.condition_id,
        "user_id": condition.user_id,
        "condition_name": condition.condition_name,
        "diagnosis_date": condition.diagnosis_date,
        "current_status": condition.current_status
    } for condition in conditions]), 200

# Read a chronic condition by ID
@chronic_condition_routes.route('/chronic_conditions/<int:condition_id>', methods=['GET'])
def get_chronic_condition_by_id(condition_id):
    condition = ChronicCondition.query.get(condition_id)
    if condition is None:
        return jsonify({"error": "Chronic condition not found"}), 404
    return jsonify({
        "condition_id": condition.condition_id,
        "user_id": condition.user_id,
        "condition_name": condition.condition_name,
        "diagnosis_date": condition.diagnosis_date,
        "current_status": condition.current_status
    }), 200

# Update a chronic condition by ID
@chronic_condition_routes.route('/chronic_conditions/<int:condition_id>', methods=['PUT'])
def update_chronic_condition(condition_id):
    condition = ChronicCondition.query.get(condition_id)
    if condition is None:
        return jsonify({"error": "Chronic condition not found"}), 404
    data = request.get_json()
    try:
        condition.condition_name = data.get('condition_name', condition.condition_name)
        condition.diagnosis_date = data.get('diagnosis_date', condition.diagnosis_date)
        condition.current_status = data.get('current_status', condition.current_status)
        db.session.commit()
        return jsonify({"message": "Chronic condition updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Delete a chronic condition by ID
@chronic_condition_routes.route('/chronic_conditions/<int:condition_id>', methods=['DELETE'])
def delete_chronic_condition(condition_id):
    condition = ChronicCondition.query.get(condition_id)
    if condition is None:
        return jsonify({"error": "Chronic condition not found"}), 404
    try:
        db.session.delete(condition)
        db.session.commit()
        return jsonify({"message": "Chronic condition deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
