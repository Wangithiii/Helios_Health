from flask import Blueprint, request, jsonify
from models import db, HealthLog

health_log_routes= Blueprint ('health_log_routes', __name__)

#Create a new health log
@health_log_routes.route('/health_logs', methods=['POST'])
def create_health_log():
    data = request.get_json()
    try:
        new_log = HealthLog(
            user_id=data['user_id'],
            symptom=data.get('symptom'),
            severity_level=data.get('severity_level'),
            log_date=data['log_date'],
            duration=data.get('duration'),
            notes=data.get('notes')
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Health log created successfully!", "log_id": new_log.log_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
    # Read all health logs
@health_log_routes.route('/health_logs', methods=['GET'])
def get_all_health_logs():
    logs = HealthLog.query.all()
    return jsonify([{
        "log_id": log.log_id,
        "user_id": log.user_id,
        "symptom": log.symptom,
        "severity_level": log.severity_level,
        "log_date": log.log_date,
        "duration": log.duration,
        "notes": log.notes,
        "timestamp": log.timestamp
    } for log in logs]), 200

# Read a single health log by ID
@health_log_routes.route('/health_logs/<int:log_id>', methods=['GET'])
def get_health_log(log_id):
    log = HealthLog.query.get(log_id)
    if log is None:
        return jsonify({"error": "Health log not found"}), 404
    return jsonify({
        "log_id": log.log_id,
        "user_id": log.user_id,
        "symptom": log.symptom,
        "severity_level": log.severity_level,
        "log_date": log.log_date,
        "duration": log.duration,
        "notes": log.notes,
        "timestamp": log.timestamp
    }), 200

# Update a health log by ID
@health_log_routes.route('/health_logs/<int:log_id>', methods=['PUT'])
def update_health_log(log_id):
    log = HealthLog.query.get(log_id)
    if log is None:
        return jsonify({"error": "Health log not found"}), 404
    data = request.get_json()
    try:
        log.symptom = data.get('symptom', log.symptom)
        log.severity_level = data.get('severity_level', log.severity_level)
        log.log_date = data.get('log_date', log.log_date)
        log.duration = data.get('duration', log.duration)
        log.notes = data.get('notes', log.notes)
        db.session.commit()
        return jsonify({"message": "Health log updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Delete a health log by ID
@health_log_routes.route('/health_logs/<int:log_id>', methods=['DELETE'])
def delete_health_log(log_id):
    log = HealthLog.query.get(log_id)
    if log is None:
        return jsonify({"error": "Health log not found"}), 404
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"message": "Health log deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400