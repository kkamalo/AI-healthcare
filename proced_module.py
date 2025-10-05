import json
import random

# -------------------
# Data Handling
# -------------------
def loadData(file_path='patients.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def saveData(data, file_path='patients.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def book_Appointments(patients_data, patient_name, doctor_name, time_slot):
    for patient in patients_data:
        if patient["name"].strip().lower() == patient_name.strip().lower():
            new_appointment = {"doctor": doctor_name, "time_slot": time_slot}
            patient.setdefault("appointments", []).append(new_appointment)
            return True
    return False

def get_Appointments(data, patient_name):
    for patient in data:
        if patient['name'].lower() == patient_name.lower():
            return patient.get('appointments', [])
    return []

# -------------------
# Predictive Risk Scoring (simple demo)
# -------------------
import random

def predict_risk(patient_age, condition):
    # Dummy scoring logic: older age + certain conditions → higher risk
    risk_base = 0
    if patient_age > 60:
        risk_base += 2
    if any(keyword in condition.lower() for keyword in ["cancer", "cardio", "heart", "critical"]):
        risk_base += 3
    # Random small variation
    return min(risk_base + random.randint(0,2), 5)
