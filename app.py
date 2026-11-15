
import streamlit as st
from supabase import create_client
from datetime import date

# ---------------- PAGE SETTINGS ----------------

import streamlit as st
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="CareCircle",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- PREMIUM CARECIRCLE DESIGN ----------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f4fbf7,
            #edf7f1
        );
        color: #183b2b;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #123d2b;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #145c3a !important;
        font-weight: 750 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #16834b;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1rem;
        font-weight: 650;
    }

    .stButton > button:hover {
        background-color: #0d6036;
        color: white;
        border: none;
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Dashboard metric cards */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #dceee3;
        box-shadow: 0 4px 14px rgba(20, 92, 58, 0.06);
    }

    [data-testid="stMetricValue"] {
        color: #16834b;
        font-weight: 800;
    }

    /* Forms */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #dceee3;
    }

    /* Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)










# ---------------- SESSION STATE ----------------

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ---------------- SUPABASE CONNECTION ----------------

try:
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    supabase = st.session_state.supabase_client

except Exception as e:
    st.error("Could not connect to Supabase. Please check Streamlit Secrets.")
    st.stop()


def get_value(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


# ---------------- DATABASE FUNCTIONS ----------------

def get_data(table):
    try:
        response = (
            supabase.table(table)
            .select("*")
            .eq("user_id", st.session_state.user_id)
            .execute()
        )
        return response.data or []
    except Exception as e:
        st.error(f"Could not load {table}: {e}")
        return []


def add_data(table, values):
    try:
        values["user_id"] = st.session_state.user_id
        supabase.table(table).insert(values).execute()
        return True
    except Exception as e:
        st.error(f"Could not save information: {e}")
        return False


def delete_data(table, row_id):
    try:
        (
            supabase.table(table)
            .delete()
            .eq("id", row_id)
            .eq("user_id", st.session_state.user_id)
            .execute()
        )
        return True
    except Exception as e:
        st.error(f"Could not delete information: {e}")
        return False


def update_medication(row_id, new_status):
    try:
        (
            supabase.table("Medications")
            .update({"status": new_status})
            .eq("id", row_id)
            .eq("user_id", st.session_state.user_id)
            .execute()
        )
        return True
    except Exception as e:
        st.error(f"Could not update medication: {e}")
        return False


# ---------------- LOGIN / SIGN UP ----------------

if st.session_state.user_id is None:

    st.title("💚 CareCircle")
    st.subheader("Care, connection and peace of mind")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        st.markdown("### Welcome back")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", use_container_width=True)

        if login_button:
            if not email or not password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    result = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    auth_user = get_value(result, "user")
                    user_id = get_value(auth_user, "id")

                    if user_id:
                        st.session_state.user_id = str(user_id)
                        st.session_state.user_email = email
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Login failed. Please check your details.")

                except Exception as e:
                    st.error(f"Login error: {e}")

    with signup_tab:
        st.markdown("### Create your account")

        with st.form("signup_form"):
            new_email = st.text_input("Email address")
            new_password = st.text_input(
                "Create password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            signup_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if signup_button:
            if not new_email or not new_password:
                st.warning("Please complete all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(new_password) < 6:
                st.error("Password must contain at least 6 characters.")
            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": new_email,
                        "password": new_password
                    })

                    auth_user = get_value(result, "user")
                    user_id = get_value(auth_user, "id")

                    if user_id:
                        st.success(
                            "Account created! Please go to Login and sign in."
                        )
                    else:
                        st.error(
                            "Account was not created. Please try again."
                        )

                except Exception as e:
                    st.error(f"Sign-up error: {e}")

    st.stop()


# ---------------- MAIN APP ----------------

st.sidebar.title("💚 CareCircle")
st.sidebar.caption("Your care coordination space")
st.sidebar.write(f"Logged in: {st.session_state.user_email}")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Medications",
        "Appointments",
        "Care Circle",
        "Activity Feed"
    ]
)

if st.sidebar.button("Logout", use_container_width=True):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.pop("supabase_client", None)
    st.rerun()


# ---------------- LOAD DATA ----------------

medications = get_data("Medications")
appointments = get_data("appoinments")
members = get_data("Members")


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("💚 CareCircle Dashboard")
    st.write("A simple space to coordinate everyday care.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Medications", len(medications))

    with col2:
        st.metric("Appointments", len(appointments))

    with col3:
        st.metric("Care Circle Members", len(members))

    st.divider()

    st.subheader("Medication Overview")

    if medications:
        for med in medications:
            st.write(
                f"💊 **{med.get('name', 'Medicine')}** — "
                f"{med.get('scheduled_time', 'Time not set')} "
                f"| Status: {med.get('status', 'Pending')}"
            )
    else:
        st.info("No medications added yet.")

    st.subheader("Upcoming Appointments")

    if appointments:
        for appointment in appointments:
            st.write(
                f"📅 **{appointment.get('title', 'Appointment')}** — "
                f"{appointment.get('date', '')} "
                f"at {appointment.get('time', '')}"
            )
    else:
        st.info("No appointments added yet.")

    st.caption(
        "CareCircle is a demonstration app. Medication statuses are "
        "user-reported and are not independently verified."
    )


# ---------------- MEDICATIONS ----------------

elif page == "Medications":

    st.title("💊 Medication Management")
    st.write("Keep track of medication information.")

    with st.form("add_medication_form"):
        medicine_name = st.text_input("Medication name")
        scheduled_time = st.text_input("Scheduled time")
        notes = st.text_area("Notes")
        add_medicine = st.form_submit_button("Add Medication")

    if add_medicine:
        if not medicine_name.strip():
            st.warning("Please enter a medication name.")
        else:
            success = add_data(
                "Medications",
                {
                    "name": medicine_name.strip(),
                    "scheduled_time": scheduled_time.strip(),
                    "notes": notes.strip(),
                    "status": "Pending"
                }
            )
            if success:
                st.success("Medication added!")
                st.rerun()

    st.divider()
    st.subheader("Your Medications")

    medications = get_data("Medications")

    if not medications:
        st.info("No medications have been added.")
    else:
        for med in medications:
            with st.container(border=True):
                st.write(f"### 💊 {med.get('name', 'Medication')}")
                st.write(
                    f"Scheduled time: {med.get('scheduled_time', 'Not set')}"
                )
                st.write(f"Notes: {med.get('notes', '')}")
                st.write(f"Status: {med.get('status', 'Pending')}")

                status_options = ["Pending", "Recorded"]

                current_status = med.get("status", "Pending")
                if current_status not in status_options:
                    current_status = "Pending"

                selected_status = st.selectbox(
                    "Update status",
                    status_options,
                    index=status_options.index(current_status),
                    key=f"status_{med.get('id')}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Save Status",
                        key=f"save_{med.get('id')}"
                    ):
                        if update_medication(
                            med.get("id"),
                            selected_status
                        ):
                            st.success("Status updated!")
                            st.rerun()

                with col2:
                    if st.button(
                        "Delete",
                        key=f"delete_med_{med.get('id')}"
                    ):
                        if delete_data("Medications", med.get("id")):
                            st.success("Medication deleted.")
                            st.rerun()


# ---------------- APPOINTMENTS ----------------

elif page == "Appointments":

    st.title("📅 Appointments")
    st.write("Keep important appointments organised.")

    with st.form("appointment_form"):
        title = st.text_input("Appointment title")
        appointment_date = st.date_input("Appointment date", value=date.today())
        appointment_time = st.text_input("Appointment time")
        details = st.text_area("Details")
        add_appointment = st.form_submit_button("Add Appointment")

    if add_appointment:
        if not title.strip():
            st.warning("Please enter an appointment title.")
        else:
            success = add_data(
                "appoinments",
                {
                    "title": title.strip(),
                    "date": str(appointment_date),
                    "time": appointment_time.strip(),
                    "details": details.strip()
                }
            )
            if success:
                st.success("Appointment added!")
                st.rerun()

    st.divider()
    st.subheader("Your Appointments")

    appointments = get_data("appoinments")

    if not appointments:
        st.info("No appointments added yet.")
    else:
        for appointment in appointments:
            with st.container(border=True):
                st.write(f"### 📅 {appointment.get('title', 'Appointment')}")
                st.write(f"Date: {appointment.get('date', '')}")
                st.write(f"Time: {appointment.get('time', '')}")
                st.write(f"Details: {appointment.get('details', '')}")

                if st.button(
                    "Delete Appointment",
                    key=f"delete_app_{appointment.get('id')}"
                ):
                    if delete_data("appoinments", appointment.get("id")):
                        st.success("Appointment deleted.")
                        st.rerun()


# ---------------- CARE CIRCLE ----------------

elif page == "Care Circle":

    st.title("👥 Care Circle")
    st.write("Add people who are part of the care network.")

    with st.form("member_form"):
        member_name = st.text_input("Member name")
        add_member = st.form_submit_button("Add Member")

    if add_member:
        if not member_name.strip():
            st.warning("Please enter a member name.")
        else:
            success = add_data(
                "Members",
                {"name": member_name.strip()}
            )
            if success:
                st.success("Member added!")
                st.rerun()

    st.divider()
    st.subheader("Your Care Circle")

    members = get_data("Members")

    if not members:
        st.info("No members added yet.")
    else:
        for member in members:
            with st.container(border=True):
                st.write(f"👤 **{member.get('name', 'Member')}**")

                if st.button(
                    "Remove Member",
                    key=f"remove_member_{member.get('id')}"
                ):
                    if delete_data("Members", member.get("id")):
                        st.success("Member removed.")
                        st.rerun()


# ---------------- ACTIVITY FEED ----------------

elif page == "Activity Feed":

    st.title("📋 Activity Feed")
    st.write("A simple overview of information saved in CareCircle.")

    st.subheader("Recent Medication Records")

    if medications:
        for med in reversed(medications):
            st.write(
                f"💊 {med.get('name', 'Medication')} — "
                f"{med.get('status', 'Pending')}"
            )
    else:
        st.info("No medication activity yet.")

    st.divider()
    st.subheader("Appointment Records")

    if appointments:
        for appointment in reversed(appointments):
            st.write(
                f"📅 {appointment.get('title', 'Appointment')} — "
                f"{appointment.get('date', '')}"
            )
    else:
        st.info("No appointment activity yet.")

    st.divider()
    st.subheader("Care Circle Updates")

    if members:
        for member in reversed(members):
            st.write(f"👤 {member.get('name', 'Member')} is in your Care Circle.")
    else:
        st.info("No Care Circle members yet.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "💚 CareCircle | Hackathon Demonstration Project | "
    "Uses fictional demo information. Not a medical or clinical system."
)
