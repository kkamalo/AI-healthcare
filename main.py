import streamlit as st
from OOP_module import Doctor
from proced_module import loadData, saveData, book_Appointments, get_Appointments, predict_risk
from functional_module import recommend_doctor, get_doctor_names
import pandas as pd

st.set_page_config(
    page_title="Smart Healthcare Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# CSS for professional look
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
    background-color: #f8f9fa;
    color: #000000;
}

.stButton>button {
    background-color: #0073e6;
    color: white;
    border-radius: 8px;
    height: 40px;
    width: 100%;
    font-weight: 500;
    border: none;
}

.stButton>button:hover {
    background-color: #005bb5;
    color: white;
}

.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

h1, h2, h3, h4 {
    color: #0073e6;
}

.metric-container {
    background-color:#ffffff;
    padding:15px;
    border-radius:10px;
    text-align:center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load Data
# ---------------------------
PATIENTS_FILE = "patients.json"
patients_data = loadData(PATIENTS_FILE)

doctors = [
    Doctor("doc_001", "Dr. Mohammed", "Plastic Surgery"),
    Doctor("doc_002", "Dr. Kety", "Physio Therapy"),
    Doctor("doc_003", "Dr. Leena", "Pediatrics"),
    Doctor("doc_004", "Dr. Aya", "Cardiology")
]

# ---------------------------
# Sidebar Menu
# ---------------------------
st.sidebar.title("🩺 Smart Healthcare Assistant")
menu = st.sidebar.radio(
    "Navigation",
    ["💬 Chat Assistant", "➕ Register Patient", "📅 Book Appointment", "📋 View Appointments", "📊 Dashboard"]
)

# ---------------------------
# Chat Assistant
# ---------------------------
if menu == "💬 Chat Assistant":
    st.title("💬 AI Healthcare Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_area("Describe patient's condition or symptoms...")
    if st.button("Recommend Doctor"):
        if user_input:
            doc_name = recommend_doctor(doctors, user_input)
            st.success(f"Recommended doctor: {doc_name}")
        else:
            st.warning("Please enter patient condition.")

# ---------------------------
# Register Patient
# ---------------------------
elif menu == "➕ Register Patient":
    st.title("➕ Register Patient")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Patient Name")
            age = st.number_input("Patient Age", min_value=0, max_value=120)
        with col2:
            condition = st.text_input("Patient Condition")

        if st.button("Register"):
            if name and condition:
                risk = predict_risk(age, condition)
                new_patient = {
                    "name": name,
                    "age": age,
                    "condition": condition,
                    "appointments": [],
                    "risk_score": risk
                }
                patients_data.append(new_patient)
                saveData(patients_data, PATIENTS_FILE)
                st.success(f"Patient '{name}' registered! Risk score: {risk}/5")
            else:
                st.error("Fill all fields.")

# ---------------------------
# Book Appointment
# ---------------------------
elif menu == "📅 Book Appointment":
    st.title("📅 Book Appointment")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            pname = st.text_input("Patient Name")
        with col2:
            dname = st.selectbox("Choose Doctor", get_doctor_names(doctors))
        with col3:
            time = st.time_input("Preferred Time Slot")

        if st.button("Book Appointment"):
            success = book_Appointments(patients_data, pname, dname, str(time))
            if success:
                saveData(patients_data, PATIENTS_FILE)
                st.success(f"Appointment booked for {pname} with {dname} at {time}")
            else:
                st.error("Patient not found.")

# ---------------------------
# View Appointments
# ---------------------------
elif menu == "📋 View Appointments":
    st.title("📋 View Appointments")
    search_name = st.text_input("Enter Patient Name")
    if st.button("Search"):
        appts = get_Appointments(patients_data, search_name)
        if appts:
            for a in appts:
                st.info(f"Doctor: {a.get('doctor')} | Time: {a.get('time_slot')}")
        else:
            st.warning("No appointments found.")

# ---------------------------
# Dashboard
# ---------------------------
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", len(patients_data))
    col2.metric("High-Risk Patients", sum(1 for p in patients_data if p.get("risk_score",0)>=3))
    col3.metric("Doctors Available", len([d for d in doctors if d.available]))

    st.markdown("---")
    st.subheader("Patient Risk Distribution")
    if patients_data:
        risk_counts = [p.get("risk_score",0) for p in patients_data]
        st.bar_chart(risk_counts)

    st.markdown("---")
    st.subheader("Appointments per Doctor")
    doctor_counts = {doc.name:0 for doc in doctors}
    for patient in patients_data:
        for a in patient.get("appointments",[]):
            doctor_counts[a["doctor"]] +=1
    st.bar_chart(doctor_counts)

    st.markdown("---")
    st.subheader("All Patients Table")
    if patients_data:
        df = pd.DataFrame(patients_data)
        st.dataframe(df)
