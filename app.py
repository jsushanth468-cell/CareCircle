import streamlit as st
from datetime import time

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide"
)

# Store demo data during the session
if "medications" not in st.session_state:
    st.session_state.medications = []

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

# Dashboard
if page == "Dashboard":
    st.title("Welcome to CareCircle 👋")
    st.write("Your family care dashboard.")

    total = len(st.session_state.medications)
    recorded = sum(
        1 for m in st.session_state.medications
        if m["status"] == "Recorded"
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Medication Records", total)
    c2.metric("Recorded Doses", recorded)
    c3.metric("Care Team Members", "3")

    st.divider()
    st.subheader("💊 Medication Overview")

    if total == 0:
        st.info("No medication records added yet.")
    else:
        for med in st.session_state.medications:
            st.write(
                f"**{med['name']}** — {med['time']} — {med['status']}"
            )

    st.info("CareCircle demo uses fictional information.")

# Medication Manager
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
                    if st.button("Delete", key=f"delete_{i}"):
                        st.session_state.medications.pop(i)
                        st.rerun()

    st.caption(
        "Recording a dose is a user-reported action, "
        "not confirmation of medical adherence."
    )

# Appointments
elif page == "Appointments":
    st.title("📅 Appointments")
    st.info("Appointment management is our next feature.")

# Care Circle
elif page == "Care Circle":
    st.title("👨‍👩‍👧 Family Care Circle")
    st.info("Family and caregiver collaboration is coming next.")
