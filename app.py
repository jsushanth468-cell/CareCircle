import streamlit as st
from datetime import date, time

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide"
)

if "medications" not in st.session_state:
    st.session_state.medications = []

if "appointments" not in st.session_state:
    st.session_state.appointments = []

if "members" not in st.session_state:
    st.session_state.members = []

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

st.title("💚 CareCircle")
st.caption("Connected care for every family")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Medications", "Appointments", "Care Circle", "Activity"]
)

if page == "Dashboard":
    st.header("Your Care Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Medication Records", len(st.session_state.medications))
    col2.metric("Appointments", len(st.session_state.appointments))
    col3.metric("Care Circle Members", len(st.session_state.members))

    st.subheader("Recent Medication Records")

    if st.session_state.medications:
        for i, med in enumerate(st.session_state.medications):
            st.write(f"💊 {med['name']} — {med['time']} — {med['status']}")
    else:
        st.info("No medication records yet.")

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
                    "name": name,
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
        with st.container(border=True):
            st.write(f"**{med['name']}**")
            st.write(f"Time: {med['time']}")
            st.write(f"Status: {med['status']}")

            col1, col2 = st.columns(2)

            if col1.button("Mark as Recorded", key=f"record_{i}"):
                st.session_state.medications[i]["status"] = "Recorded"
                st.rerun()

            if col2.button("Delete", key=f"delete_med_{i}"):
                st.session_state.medications.pop(i)
                st.rerun()

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
                    "title": title,
                    "date": str(appointment_date),
                    "time": appointment_time.strftime("%I:%M %p"),
                    "details": details
                })
                st.success("Appointment added!")
                st.rerun()
            else:
                st.warning("Please enter an appointment title.")

    for i, appointment in enumerate(st.session_state.appointments):
        with st.container(border=True):
            st.write(f"**{appointment['title']}**")
            st.write(f"Date: {appointment['date']}")
            st.write(f"Time: {appointment['time']}")
            st.write(appointment["details"])

            if st.button("Delete Appointment", key=f"delete_appointment_{i}"):
                st.session_state.appointments.pop(i)
                st.rerun()

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
                st.warning("Enter a name.")

    for i, member in enumerate(st.session_state.members):
        col1, col2 = st.columns([4, 1])
        col1.write(f"👤 {member}")

        if col2.button("Remove", key=f"remove_{i}"):
            st.session_state.members.pop(i)
            st.rerun()

elif page == "Activity":
    st.header("📋 Activity Feed")

    if not st.session_state.medications and not st.session_state.appointments:
        st.info("No activity to display yet.")
    else:
        for med in st.session_state.medications:
            st.write(f"💊 {med['name']} — {med['status']}")

        for appointment in st.session_state.appointments:
            st.write(f"📅 {appointment['title']} — {appointment['date']}")

st.divider()
st.caption("💚 CareCircle | Connected care for every family | Demonstration application")
