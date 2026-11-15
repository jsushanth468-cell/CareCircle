
import streamlit as st
from datetime import time, date

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide"
)

# Session storage
if "medications" not in st.session_state:
    st.session_state.medications = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

# Styling
st.markdown("""
<style>
.stApp {
    background-color: #f5f9f6;
}
h1, h2, h3 {
    color: #174d38;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #dcebe1;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("💚 CareCircle")
    st.caption("Connected care for every family")

    page = st.radio(
        "Navigation",
        ["Dashboard", "Medications", "Appointments", "Care Circle"]
    )

# DASHBOARD
if page == "Dashboard":
    st.title("Welcome to CareCircle 👋")
    st.write("Your family care dashboard.")

    total_meds = len(st.session_state.medications)
    recorded = sum(
        1 for m in st.session_state.medications
        if m["status"] == "Recorded"
    )
    total_appointments = len(st.session_state.appointments)

    c1, c2, c3 = st.columns(3)

    c1.metric("Medication Records", total_meds)
    c2.metric("Recorded Doses", recorded)
    c3.metric("Appointments", total_appointments)

    st.divider()
    st.subheader("💊 Medication Overview")

    if total_meds == 0:
        st.info("No medication records added yet.")
    else:
        for med in st.session_state.medications:
            st.write(
                f"**{med['name']}** — {med['time']} — {med['status']}"
            )

    st.divider()
    st.subheader("📅 Upcoming Appointments")

    if total_appointments == 0:
        st.info("No appointments added yet.")
    else:
        for appointment in st.session_state.appointments:
            st.write(
                f"**{appointment['doctor']}** — "
                f"{appointment['date']} at {appointment['time']}"
            )

    st.caption("CareCircle demo uses fictional information.")

# MEDICATION MANAGER
elif page == "Medications":
    st.title("💊 Medication Manager")
    st.write("Add and manage medication schedule records.")

    with st.form("medication_form"):
        name = st.text_input("Medication name")
        scheduled_time = st.time_input(
            "Scheduled time",
            value=time(8, 0)
        )
        notes = st.text_input("Optional note")

        submitted = st.form_submit_button("Add Medication")

        if submitted:
            if name.strip():
                st.session_state.medications.append({
                    "name": name.strip(),
                    "time": scheduled_time.strftime("%I:%M %p"),
                    "notes": notes.strip(),
                    "status": "Pending"
                })
                st.success("Medication record added!")
            else:
                st.error("Please enter a medication name.")

    st.divider()
    st.subheader("Saved Medication Records")

    if not st.session_state.medications:
        st.info("Your medication list is currently empty.")
    else:
        for i, med in enumerate(st.session_state.medications):
            with st.container(border=True):
                st.write(f"### {med['name']}")
                st.write(f"Scheduled time: {med['time']}")

                if med["notes"]:
                    st.caption(med["notes"])

                st.write(f"Status: **{med['status']}**")

                col1, col2 = st.columns(2)

                with col1:
                    if med["status"] == "Pending":
                        if st.button(
                            "Mark as Recorded",
                            key=f"record_{i}"
                        ):
                            st.session_state.medications[i]["status"] = "Recorded"
                            st.rerun()

                with col2:
                    if st.button("Delete", key=f"delete_med_{i}"):
                        st.session_state.medications.pop(i)
                        st.rerun()

    st.caption(
        "Recording a dose is a user-reported action, "
        "not confirmation of medical adherence."
    )

# APPOINTMENT MANAGER
elif page == "Appointments":
    st.title("📅 Appointments Manager")
    st.write("Organise and manage healthcare appointments.")

    with st.form("appointment_form"):
        doctor = st.text_input("Doctor or Hospital Name")

        appointment_date = st.date_input(
            "Appointment Date",
            value=date.today()
        )

        appointment_time = st.time_input(
            "Appointment Time",
            value=time(10, 0)
        )

        details = st.text_area("Appointment Details or Notes")

        submitted = st.form_submit_button("Add Appointment")

        if submitted:
            if doctor.strip():
                st.session_state.appointments.append({
                    "doctor": doctor.strip(),
                    "date": appointment_date.strftime("%d %B %Y"),
                    "time": appointment_time.strftime("%I:%M %p"),
                    "details": details.strip()
                })
                st.success("Appointment added successfully!")
            else:
                st.error("Please enter a doctor or hospital name.")

    st.divider()
    st.subheader("Your Saved Appointments")

    if not st.session_state.appointments:
        st.info("No appointments added yet.")
    else:
        for i, appointment in enumerate(
            st.session_state.appointments
        ):
            with st.container(border=True):
                st.write(f"### 🏥 {appointment['doctor']}")
                st.write(f"Date: {appointment['date']}")
                st.write(f"Time: {appointment['time']}")

                if appointment["details"]:
                    st.caption(appointment["details"])

                if st.button(
                    "Delete Appointment",
                    key=f"delete_appointment_{i}"
                ):
                    st.session_state.appointments.pop(i)
                    st.rerun()

# CARE CIRCLE
elif page == "Care Circle":
    st.title("👨‍👩‍👧 Family Care Circle")
    st.write("Connect family members and caregivers.")
    st.info("Family collaboration features are coming next.")
