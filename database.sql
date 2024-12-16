/*Tables*/

CREATE TABLE users(
user_id INT PRIMARY KEY AUTO_INCREMENT,
first_name VARCHAR(255) NOT NULL,
last_name VARCHAR(255) NOT NULL,
email_address VARCHAR (255) UNIQUE,
phone_number VARCHAR (50)
password_hash VARCHAR(255),
date_of_birth DATE,
gender ENUM('Male', 'Female', 'Other'),
medical_history TEXT,
allergies TEXT,
chronic_conditions TEXT
);

/*Symptoms Log*/

CREATE TABLE health_logs(
log_id INT PRIMARY KEY AUTO_INCREMENT,
user_id INT,
symptom VARCHAR(255),
severity_level ENUM('Mild', 'Moderate', 'Severe'),
log_date DATE NOT NULL,
duration INT,
notes TEXT,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(user_id)
);

/*Medications*/ 
CREATE TABLE medications (
medication_id INT PRIMARY KEY AUTO_INCREMENT,
user_id INT, 
medication_name VARCHAR(255) NOT NULL,
dosage VARCHAR(255) NOT NULL,
frequency VARCHAR(255) NOT  NULL,
start_date DATE NOT NULL, 
end_date DATE,
notes TEXT,
FOREIGN KEY (user_id) REFERENCES users (user_id)
);


/*Chronic Conditions*/
CREATE TABLE chronic_conditions(
condition_id INT PRIMARY KEY  AUTO_INCREMENT,
user_id INT,
condition_name VARCHAR (255),
diagnosis_date DATE,
current_status VARCHAR (255),
FOREIGN KEY (user_id) REFERENCES users(user_id)
);

/*Specialists*/
CREATE TABLE specialists(
specialist_id INT PRIMARY KEY AUTO_INCREMENT,
specialty VARCHAR(100) NOT NULL,
first_name VARCHAR (255) NOT NULL,
last_name VARCHAR(255) NOT NULL,
phone_number INT NOT NULL,
email_address VARCHAR(255) NOT NULL,
available_times TEXT
);



