from typing import List
from OOP_module import Doctor

# Recommend doctors based on patient condition + availability
def recommend_doctor(doctors: List[Doctor], patient_condition: str) -> str:
    # simple keyword matching
    for doc in doctors:
        if doc.available and doc.specialty.lower() in patient_condition.lower():
            return doc.name
    # fallback to any available doctor
    for doc in doctors:
        if doc.available:
            return doc.name
    return "No doctors available"

# Get available doctor names
def get_doctor_names(doctors: List[Doctor]) -> List[str]:
    return [doc.name for doc in doctors if doc.available]
