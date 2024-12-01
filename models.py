from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

# Enums for reusable values
class GenderEnum(PyEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

class SeverityEnum(PyEnum):
    MILD = 'Mild'
    MODERATE = 'Moderate'
    SEVERE = 'Severe'

# User Model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email_address = db.Column(db.String(255), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)  # Changed from Integer
    password_hash = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    chronic_conditions = db.Column(db.Text, nullable=True)

    # Relationships
    health_logs = db.relationship('HealthLog', backref='user', lazy=True)
    medications = db.relationship('Medication', backref='user', lazy=True)
    chronic_conditions_list = db.relationship('ChronicCondition', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

# Health Log Model
class HealthLog(db.Model):
    __tablename__ = 'health_logs'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    symptom = db.Column(db.String(255), nullable=True)
    severity_level = db.Column(db.String(50), nullable=True)
    log_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # Optional
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"<HealthLog {self.log_id} - {self.symptom}>"

# Medication Model
class Medication(db.Model):
    __tablename__ = 'medications'

    medication_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    medication_name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Medication {self.medication_name}>"

# Chronic Condition Model
class ChronicCondition(db.Model):
    __tablename__ = 'chronic_conditions'

    condition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    condition_name = db.Column(db.String(255), nullable=True)
    diagnosis_date = db.Column(db.Date, nullable=True)
    current_status = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<ChronicCondition {self.condition_name}>"

# Specialist Model
class Specialist(db.Model):
    __tablename__ = 'specialists'

    specialist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specialty = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email_address = db.Column(db.String(255), nullable=False)
    available_times = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Specialist {self.first_name} {self.last_name} - {self.specialty}>"
