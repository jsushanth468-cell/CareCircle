
import streamlit as st
from supabase import create_client
from datetime import date, time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4faf6;
}
h1, h2, h3 {
    color: #176b50;
}
.stButton button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SUPABASE CONNECTION ----------------

try:
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    supabase = st.session_state.supabase_client

except Exception as e:
    st.error("Supabase connection failed. Check Streamlit Secrets.")
    st.stop()




# ---------------- AUTHENTICATION ----------------

def login_page():

    st.title("💚 CareCircle")
    st.subheader("Your family care management dashboard")
    st.write("Sign in or create an account to continue.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input(
                "Password",
                type="password"
            )
            login_button = st.form_submit_button("Login")

        if login_button:
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                st.session_state.user_id = result.user.id
                st.session_state.user_email = result.user.email

                st.success("Login successful!")
                st.rerun()

            except Exception:
                st.error("Login failed. Check your email and password.")

    with signup_tab:
        with st.form("signup_form"):
            new_email = st.text_input("Your email")
            new_password = st.text_input(
                "Create password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )

            signup_button = st.form_submit_button("Create Account")

        if signup_button:
            if not new_email or not new_password:
                st.warning("Please fill in all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": new_email,
                        "password": new_password
                    })

                    if result.session:
                        st.session_state.user_id = result.user.id
                        st.session_state.user_email = result.user.email
                        st.success("Account created!")
                        st.rerun()
                    else:
                        st.success(
                            "Account created! Check your email "
                            "for confirmation, then log in."
                        )

                except Exception as e:
                    st.error(f"Sign-up failed: {e}")


if not st.session_state.user_id:
    login_page()
    st.stop()


# ---------------- USER DETAILS ----------------

user_id = st.session_state.user_id

st.sidebar.title("💚 CareCircle")
st.sidebar.caption(st.session_state.user_email)

if st.sidebar.button("Logout"):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.user_id = None
    st.session_state.user_email = None
    st.rerun()


# ---------------- DATABASE FUNCTIONS ----------------

def get_data(table):
    return (
        supabase.table(table)
        .select("*")
        .eq("user_id", user_id)
        .execute()
        .data
    )


def add_data(table, values):
    values["user_id"] = user_id
    return supabase.table(table).insert(values).execute()


def delete_data(table, row_id):
    return (
        supabase.table(table)
        .delete()
        .eq("id", row_id)
        .eq("user_id", user_id)
        .execute()
    )


def update_medication(row_id, new_status):
    return (
        supabase.table("Medications")
        .update({"status": new_status})
        .eq("id", row_id)
        .eq("user_id", user_id)
        .execute()
    )


# ---------------- NAVIGATION ----------------

section = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Medications",
        "Appointments",
        "Care Circle",
        "Activity"
    ]
)

st.title("💚 CareCircle")


# ---------------- DASHBOARD ----------------

if section == "Dashboard":

    st.subheader("Welcome to your dashboard!")

    try:
        medications = get_data("Medications")
        appointments = get_data("appoinments")
        members = get_data("Members")

        col1, col2, col3 = st.columns(3)

        col1.metric("Medications", len(medications))
        col2.metric("Appointments", len(appointments))
        col3.metric("Care Circle Members", len(members))

        st.divider()

        st.subheader("Medication Overview")

        if medications:
            for med in medications:
                st.write(
                    f"💊 **{med['name']}** — "
                    f"{med['scheduled_time']} — "
                    f"{med['status']}"
                )
        else:
            st.info("No medications added yet.")

        st.subheader("Upcoming Appointments")

        if appointments:
            for appt in appointments:
                st.write(
                    f"📅 **{appt['title']}** — "
                    f"{appt['date']} at {appt['time']}"
                )
        else:
            st.info("No appointments added yet.")

    except Exception as e:
        st.error(f"Dashboard error: {e}")


# ---------------- MEDICATIONS ----------------

elif section == "Medications":

    st.subheader("💊 Medication Management")

    with st.form("medication_form"):
        name = st.text_input("Medication name")
        scheduled_time = st.time_input(
            "Scheduled time",
            value=time(9, 0)
        )
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add Medication")

    if submitted:
        if name.strip():
            try:
                add_data("Medications", {
                    "name": name.strip(),
                    "scheduled_time": scheduled_time.strftime("%H:%M"),
                    "notes": notes,
                    "status": "Pending"
                })
                st.success("Medication added!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not add medication: {e}")
        else:
            st.warning("Enter a medication name.")

    st.divider()
    st.subheader("Your Medications")

    try:
        medications = get_data("Medications")

        if not medications:
            st.info("No medications added yet.")

        for med in medications:
            with st.container(border=True):
                st.write(f"**{med['name']}**")
                st.write(f"Time: {med['scheduled_time']}")
                st.write(f"Notes: {med.get('notes') or 'None'}")
                st.write(f"Status: {med['status']}")

                col1, col2 = st.columns(2)

                if col1.button(
                    "Mark as Recorded",
                    key=f"record_{med['id']}"
                ):
                    update_medication(med["id"], "Recorded")
                    st.rerun()

                if col2.button(
                    "Delete",
                    key=f"delete_med_{med['id']}"
                ):
                    delete_data("Medications", med["id"])
                    st.rerun()

    except Exception as e:
        st.error(f"Could not load medications: {e}")


# ---------------- APPOINTMENTS ----------------

elif section == "Appointments":

    st.subheader("📅 Appointment Management")

    with st.form("appointment_form"):

        title = st.text_input("Appointment title")
        appointment_date = st.date_input(
            "Appointment date",
            value=date.today()
        )
        appointment_time = st.time_input(
            "Appointment time",
            value=time(10, 0)
        )
        details = st.text_area("Appointment details")

        submitted = st.form_submit_button("Add Appointment")

    if submitted:
        if title.strip():
            try:
                add_data("appoinments", {
                    "title": title.strip(),
                    "date": appointment_date.isoformat(),
                    "time": appointment_time.strftime("%H:%M"),
                    "details": details
                })

                st.success("Appointment added!")
                st.rerun()

            except Exception as e:
                st.error(f"Could not add appointment: {e}")
        else:
            st.warning("Enter an appointment title.")

    st.divider()
    st.subheader("Your Appointments")

    try:
        appointments = get_data("appoinments")

        if not appointments:
            st.info("No appointments added yet.")

        for appt in appointments:
            with st.container(border=True):
                st.write(f"**{appt['title']}**")
                st.write(f"Date: {appt['date']}")
                st.write(f"Time: {appt['time']}")
                st.write(
                    f"Details: {appt.get('details') or 'None'}"
                )

                if st.button(
                    "Delete Appointment",
                    key=f"delete_appt_{appt['id']}"
                ):
                    delete_data("appoinments", appt["id"])
                    st.rerun()

    except Exception as e:
        st.error(f"Could not load appointments: {e}")


# ---------------- CARE CIRCLE ----------------

elif section == "Care Circle":

    st.subheader("👨‍👩‍👧 Care Circle Members")

    with st.form("member_form"):
        member_name = st.text_input("Member name")
        submitted = st.form_submit_button("Add Member")

    if submitted:
        if member_name.strip():
            try:
                add_data("Members", {
                    "name": member_name.strip()
                })
                st.success("Member added!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not add member: {e}")
        else:
            st.warning("Enter a member name.")

    st.divider()

    try:
        members = get_data("Members")

        if not members:
            st.info("No members added yet.")

        for member in members:
            col1, col2 = st.columns([4, 1])

            col1.write(f"👤 {member['name']}")

            if col2.button(
                "Remove",
                key=f"remove_{member['id']}"
            ):
                delete_data("Members", member["id"])
                st.rerun()

    except Exception as e:
        st.error(f"Could not load members: {e}")


# ---------------- ACTIVITY ----------------

elif section == "Activity":

    st.subheader("📋 Activity Overview")

    try:
        medications = get_data("Medications")
        appointments = get_data("appoinments")
        members = get_data("Members")

        st.write("### Medication Activity")

        for med in medications:
            st.write(
                f"💊 {med['name']} — {med['status']}"
            )

        st.write("### Appointment Activity")

        for appt in appointments:
            st.write(
                f"📅 {appt['title']} — {appt['date']}"
            )

        st.write("### Care Circle Activity")

        for member in members:
            st.write(f"👤 {member['name']}")

        if not medications and not appointments and not members:
            st.info("No activity recorded yet.")

    except Exception as e:
        st.error(f"Could not load activity: {e}")
        
# ---------------- SUPABASE CONNECTION ----------------

try:
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    supabase = st.session_state.supabase_client

except Exception as e:
    st.error("Supabase connection failed. Check Streamlit Secrets.")
    st.stop()

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "CareCircle | A family care management demonstration app. "
    "Medication records are user-reported, not verified."
)
