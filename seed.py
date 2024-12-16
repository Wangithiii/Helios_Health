from app import app  
from extensions import db
from faker import Faker
from datetime import datetime, timedelta
from random import choice, seed, randint 
from models import User, HealthLog, Medication, ChronicCondition, Specialist

# Initialize Faker and set a random seed for reproducibility
faker = Faker()
seed(42)

# Delete existing data to avoid duplicate entries
def clear_existing_data():
    with app.app_context():  
        db.session.query(ChronicCondition).delete()
        db.session.query(HealthLog).delete()
        db.session.query(Medication).delete()
        db.session.query(Specialist).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("Existing data cleared!")

# Seed Users with Faker
def seed_users():
    with app.app_context(): 
        users = [
            User(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email_address=faker.unique.email(),
                phone_number=faker.unique.phone_number()[:50],  # Truncate phone number to 50 characters
                date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=65),
                gender=choice(["Male", "Female", "Other"]),
                medical_history="No significant history",
                allergies="None"
            )
            for _ in range(25)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Users seeded successfully!")

# Seed Health Logs
def seed_health_logs():
    with app.app_context(): 
        users = db.session.query(User).all()
        if not users:
            print("No users found! Please seed users first.")
            return

        symptoms = ["Headache", "Fever", "Cough", "Stomach Pain", "Back Pain", "Sore Throat", "Fatigue", "Dizziness", "Rash", "Chest Pain"]

        health_logs = [
            HealthLog(
                user_id=choice(users).user_id,
                symptom=choice(symptoms),
                severity_level=choice(["Mild", "Moderate", "Severe"]),
                log_date=faker.date_between(start_date="-30d", end_date="today"),
                duration=faker.random_int(min=10, max=120),  # Duration in minutes
                notes=faker.sentence(nb_words=10)
            )
            for _ in range(25)
        ]
        db.session.bulk_save_objects(health_logs)
        db.session.commit()
        print("Health logs seeded successfully!")

# Seed Medications
def seed_medications():
    with app.app_context():
        users = db.session.query(User).all()
        if not users:
            print("No users found! Please seed users first.")
            return

        medication_names = ["Aspirin", "Ibuprofen", "Paracetamol", "Antibiotic A", "Antibiotic B"]

        medications = [
            Medication(
                user_id=choice(users).user_id,
                medication_name=choice(medication_names),
                dosage=f"{faker.random_int(min=1, max=3)} tablets",
                frequency=choice(["Once a day", "Twice a day", "Three times a day"]),
                notes=faker.sentence(nb_words=10),
                start_date = datetime.now()- timedelta(days=randint(1,30))
            )
            for _ in range(25)
        ]
        db.session.bulk_save_objects(medications)
        db.session.commit()
        print("Medications seeded successfully!")

# Seed Chronic Conditions
def seed_chronic_conditions():
    with app.app_context():
        users = db.session.query(User).all()
        if not users:
            print("No users found! Please seed users first.")
            return

        conditions = ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Arthritis", "Cancer", "Epilepsy", "Stroke", "Multiple Sclerosis", "Parkinson's Disease"]

        chronic_conditions = [
            ChronicCondition(
                user_id=choice(users).user_id,
                condition_name=choice(conditions),
                diagnosis_date=faker.date_between(start_date="-10y", end_date="today"),
                current_status=choice(["Stable", "Improving", "Worsening", "In remission"])
            )
            for _ in range(25)
        ]
        db.session.bulk_save_objects(chronic_conditions)
        db.session.commit()
        print("Chronic conditions seeded successfully!")

# Seed Specialists
def seed_specialists():
    with app.app_context():
        specialties = ["Cardiologist", "Dermatologist", "Neurologist", "Orthopedist", "Pediatrician", "Endocrinologist", "Gastroenterologist", "Psychiatrist"]

        specialists = [
            Specialist(
                specialty=choice(specialties),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                phone_number=faker.unique.phone_number()[:50],  # Truncate phone number to 50 characters
                email_address=faker.unique.email(),
                available_times=f"Weekdays {faker.random_int(min=8, max=18)}:00 to {faker.random_int(min=8, max=18)}:00"
            )
            for _ in range(25)
        ]
        db.session.bulk_save_objects(specialists)
        db.session.commit()
        print("Specialists seeded successfully!")

# Main function to run all seeding functions
def main():
    clear_existing_data()
    seed_users()
    seed_health_logs()
    seed_medications()
    seed_chronic_conditions()
    seed_specialists()
    print("Seeding completed successfully!")

if __name__ == "__main__":
    main()
