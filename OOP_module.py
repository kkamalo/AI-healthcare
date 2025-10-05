class Patient:
    def __init__(self, patientID, name, age, condition):
        self.patientID = patientID
        self.name = name
        self.age = age
        self.condition = condition
        self.appointments = []

class Doctor:
    def __init__(self, docID, name, specialty, available=True):
        self.docID = docID
        self.name = name
        self.specialty = specialty
        self.available = available
        self.appointments = []

    def book_appt(self, appointment):
        self.appointments.append(appointment)

class Appointment:
    def __init__(self, patient, doctor, time_slot):
        self.patient = patient
        self.doctor = doctor
        self.time_slot = time_slot
