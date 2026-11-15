
import streamlit as st
from datetime import date, time

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide"
)

# Initialize session data
st.session_state.setdefault("medications", [])
st.session_state.setdefault("appointments", [])
st.session_state.setdefault("members", [])

# Design
st.markdown("""
<style>
.stApp {
    background-color: #f4f8f5;
}
h1, h2, h3 {
    color: #176b50;
}
div.stButton > button {
    border-radius: 10px;
    background-color: #176b50;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("💚 CareCircle")
st.sidebar.caption("Connected care for every family")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Medications", "Appointments", "Care Circle", "Activity"]
)

st.title("💚 CareCircle")
st.caption("Connected care for every family")

# DASHBOARD
if page == "Dashboard":
    st.header("Your Care Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Medication Records", len(st.session_state.medications))
    col2.metric("Appointments", len(st.session_state.appointments))
    col3.metric("Care Circle Members", len(st.session_state.members))

    st.subheader("Recent Medication Records")

    if st.session_state.medications:
        for med in st.session_state.medications:
            if isinstance(med, dict):
                st.write(
                    f"💊 {med.get('name', 'Unnamed')} — "
                    f"{med.get('time', 'Not set')} — "
                    f"{med.get('status', 'Pending')}"
                )
    else:
        st.info("No medication records yet.")

    st.subheader("Upcoming Appointments")

    if st.session_state.appointments:
        for appointment in st.session_state.appointments:
            if isinstance(appointment, dict):
                st.write(
                    f"📅 {appointment.get('title', 'Untitled Appointment')} — "
                    f"{appointment.get('date', 'Date not set')}"
                )
    else:
        st.info("No appointments yet.")

# MEDICATIONS
elif page == "Medications":
    st.header("💊 Medication Manager")

    with st.form("medication_form"):
        name = st.text_input("Medication name")
        schedule = st.time_input("Scheduled time", value=time(8, 0))
        notes = st.text_input("Notes")

        submitted = st.form_submit_button("Add Medication")

        if submitted:
            if name.strip():
                st.session_state.medications.append({
                    "name": name.strip(),
                    "time": schedule.strftime("%I:%M %p"),
                    "notes": notes,
                    "status": "Pending"
                })
                st.success("Medication record added!")
                st.rerun()
            else:
                st.warning("Please enter a medication name.")

    st.subheader("Medication Schedule")

    for i, med in enumerate(st.session_state.medications):
        if not isinstance(med, dict):
            continue

        with st.container(border=True):
            st.write(f"**{med.get('name', 'Unnamed')}**")
            st.write(f"Time: {med.get('time', 'Not set')}")
            st.write(f"Status: {med.get('status', 'Pending')}")

            col1, col2 = st.columns(2)

            if col1.button("Mark as Recorded", key=f"record_{i}"):
                med["status"] = "Recorded"
                st.rerun()

            if col2.button("Delete", key=f"delete_med_{i}"):
                st.session_state.medications.pop(i)
                st.rerun()

# APPOINTMENTS
elif page == "Appointments":
    st.header("📅 Appointments Manager")

    with st.form("appointment_form"):
        title = st.text_input("Appointment title")
        appointment_date = st.date_input("Date", value=date.today())
        appointment_time = st.time_input("Time", value=time(10, 0))
        details = st.text_area("Additional details")

        submitted = st.form_submit_button("Add Appointment")

        if submitted:
            if title.strip():
                st.session_state.appointments.append({
                    "title": title.strip(),
                    "date": str(appointment_date),
                    "time": appointment_time.strftime("%I:%M %p"),
                    "details": details
                })
                st.success("Appointment added!")
                st.rerun()
            else:
                st.warning("Please enter an appointment title.")

    for i, appointment in enumerate(st.session_state.appointments):
        if not isinstance(appointment, dict):
            continue

        with st.container(border=True):
            st.write(
                f"**{appointment.get('title', 'Untitled Appointment')}**"
            )
            st.write(f"Date: {appointment.get('date', 'Not set')}")
            st.write(f"Time: {appointment.get('time', 'Not set')}")
            st.write(appointment.get("details", ""))

            if st.button("Delete Appointment", key=f"delete_appointment_{i}"):
                st.session_state.appointments.pop(i)
                st.rerun()

# CARE CIRCLE
elif page == "Care Circle":
    st.header("👨‍👩‍👧 Care Circle")

    with st.form("member_form"):
        member = st.text_input("Family member name")
        submitted = st.form_submit_button("Add Member")

        if submitted:
            if member.strip():
                st.session_state.members.append(member.strip())
                st.success("Member added!")
                st.rerun()
            else:
                st.warning("Please enter a name.")

    st.subheader("Family Members")

    for i, member in enumerate(st.session_state.members):
        col1, col2 = st.columns([4, 1])

        col1.write(f"👤 {member}")

        if col2.button("Remove", key=f"remove_{i}"):
            st.session_state.members.pop(i)
            st.rerun()

# ACTIVITY FEED
elif page == "Activity":
    st.header("📋 Activity Feed")
    st.caption("Overview of recorded medication entries and appointments")

    st.subheader("Medication Activity")

    if st.session_state.medications:
        for med in st.session_state.medications:
            if isinstance(med, dict):
                st.write(
                    f"💊 {med.get('name', 'Unnamed')} — "
                    f"{med.get('status', 'Pending')} — "
                    f"{med.get('time', 'Time not set')}"
                )
    else:
        st.info("No medication activity yet.")

    st.subheader("Appointment Activity")

    if st.session_state.appointments:
        for appointment in st.session_state.appointments:
            if isinstance(appointment, dict):
                appointment_title = appointment.get(
                    "title",
                    "Untitled Appointment"
                )
                appointment_date = appointment.get(
                    "date",
                    "Date not set"
                )

                st.write(
                    f"📅 {appointment_title} — {appointment_date}"
                )
    else:
        st.info("No appointment activity yet.")

    st.subheader("Care Circle Activity")

    if st.session_state.members:
        for member in st.session_state.members:
            st.write(f"👤 {member}")
    else:
        st.info("No family members added yet.")

# FOOTER
st.divider()

st.caption(
    "💚 CareCircle | Connected care for every family | "
    "Demonstration application"
)
