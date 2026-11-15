
import streamlit as st
from supabase import create_client
from datetime import date

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CareCircle | Care Together",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM DESIGN
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f4f8f5;
    color: #173b2b;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #103d2b, #092c20);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #d4ebdc !important;
}

h1, h2, h3 {
    color: #145c3a !important;
    font-weight: 800 !important;
}

p {
    color: #496454;
}

.stButton > button {
    background: linear-gradient(120deg, #16834b, #23965b);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 42px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #0c6338;
    color: white;
    border: none;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

[data-testid="stMetric"] {
    background: white;
    padding: 23px;
    border-radius: 17px;
    border: 1px solid #dcebe1;
    box-shadow: 0 5px 18px rgba(16, 61, 43, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #587465 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #16834b !important;
    font-weight: 800;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-radius: 16px;
    border: 1px solid #dcebe1;
}

div[data-testid="stForm"] {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #dcebe1;
}

hr {
    border-color: #dcebe1;
}

.small-note {
    color: #718579;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# =====================================================
# SUPABASE CONNECTION
# =====================================================

try:
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    supabase = st.session_state.supabase_client

except Exception:
    st.error("Unable to connect to CareCircle database.")
    st.info("Please check your Supabase settings in Streamlit Secrets.")
    st.stop()


def get_value(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


# =====================================================
# DATABASE FUNCTIONS
# =====================================================

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
        st.error(f"Unable to load {table}: {e}")
        return []


def add_data(table, values):
    try:
        record = dict(values)
        record["user_id"] = st.session_state.user_id

        supabase.table(table).insert(record).execute()
        return True

    except Exception as e:
        st.error(f"Unable to save information: {e}")
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
        st.error(f"Unable to delete information: {e}")
        return False


def update_medication(row_id, status):
    try:
        (
            supabase.table("Medications")
            .update({"status": status})
            .eq("id", row_id)
            .eq("user_id", st.session_state.user_id)
            .execute()
        )
        return True

    except Exception as e:
        st.error(f"Unable to update medication: {e}")
        return False


# =====================================================
# AUTHENTICATION SCREEN
# =====================================================

if st.session_state.user_id is None:

    st.markdown("""
    <div style="
        background: linear-gradient(120deg,#103d2b,#23965b);
        padding: 35px;
        border-radius: 22px;
        margin-bottom: 25px;
        text-align: center;
    ">
        <div style="font-size:45px;">💚</div>
        <h1 style="color:white !important;">
            Welcome to CareCircle
        </h1>
        <p style="color:#e0f5e7;font-size:17px;">
            Care better. Stay connected. Make every day easier.
        </p>
        <p style="color:#d0ead9;">
            Everyday care coordination, brought together.
        </p>
    </div>
    """, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(["🔐 Login", "✨ Create Account"])

    with login_tab:

        st.subheader("Welcome back")
        st.write("Sign in to continue to your care dashboard.")

        with st.form("login_form"):

            email = st.text_input("Email address")
            password = st.text_input("Password", type="password")

            login_button = st.form_submit_button(
                "Login to CareCircle",
                use_container_width=True
            )

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
                        st.success("Welcome to CareCircle!")
                        st.rerun()

                    else:
                        st.error("Login unsuccessful. Please try again.")

                except Exception as e:
                    st.error(f"Login error: {e}")

    with signup_tab:

        st.subheader("Create your account")
        st.write("Join CareCircle and organise everyday care.")

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
                            "Account created! Please log in."
                        )
                    else:
                        st.error("Account creation was unsuccessful.")

                except Exception as e:
                    st.error(f"Sign-up error: {e}")

    st.markdown("""
    <p style="text-align:center;color:#718579;">
        💚 CareCircle | Together, we care better.
    </p>
    """, unsafe_allow_html=True)

    st.stop()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown("""
<div style="text-align:center;padding:18px 5px;">
    <div style="font-size:38px;">💚</div>
    <h2 style="color:white !important;margin:0;">
        CareCircle
    </h2>
    <p style="font-size:12px;color:#d4ebdc;">
        CARE • CONNECT • COORDINATE
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

st.sidebar.caption("YOUR WORKSPACE")
st.sidebar.write(f"👤 {st.session_state.user_email}")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Medications",
        "Appointments",
        "Care Circle",
        "Activity Feed"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("""
<p style="font-size:12px;color:#cce4d5;">
    Your everyday care coordination space.
</p>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", use_container_width=True):

    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.pop("supabase_client", None)

    st.rerun()


# =====================================================
# LOAD USER DATA
# =====================================================

medications = get_data("Medications")
appointments = get_data("appoinments")
members = get_data("Members")


# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#103d2b,#23965b);
        padding:32px;
        border-radius:20px;
        margin-bottom:25px;
    ">
        <h1 style="color:white !important;">
            Welcome to CareCircle 💚
        </h1>
        <p style="color:#e0f5e7;font-size:17px;">
            Care better. Stay connected. Make every day easier.
        </p>
        <p style="color:#d0ead9;">
            Your everyday care coordination space.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Care Overview")
    st.write("A quick look at your organised care information.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💊 Medications",
            len(medications)
        )

    with col2:
        st.metric(
            "📅 Appointments",
            len(appointments)
        )

    with col3:
        st.metric(
            "👥 Care Circle Members",
            len(members)
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("💊 Medication Overview")

        if medications:

            for med in medications:

                with st.container(border=True):
                    st.write(f"**{med.get('name', 'Medication')}**")
                    st.write(
                        f"Time: {med.get('scheduled_time', 'Not set')}"
                    )

                    status = med.get("status", "Pending")

                    if status == "Recorded":
                        st.success("Recorded")
                    else:
                        st.info("Pending")

        else:
            st.info("No medication records yet.")

    with right:

        st.subheader("📅 Upcoming Appointments")

        if appointments:

            for appointment in appointments:

                with st.container(border=True):
                    st.write(
                        f"**{appointment.get('title', 'Appointment')}**"
                    )
                    st.write(
                        f"Date: {appointment.get('date', 'Not set')}"
                    )
                    st.write(
                        f"Time: {appointment.get('time', 'Not set')}"
                    )

        else:
            st.info("No appointments added yet.")

    st.divider()

    st.subheader("👥 Your Care Circle")

    if members:

        member_columns = st.columns(3)

        for index, member in enumerate(members):

            with member_columns[index % 3]:
                with st.container(border=True):
                    st.markdown("### 👤")
                    st.write(f"**{member.get('name', 'Member')}**")

    else:
        st.info("Add members to your Care Circle.")

    st.caption(
        "CareCircle is a demonstration project. "
        "Medication statuses are user-reported and not independently verified."
    )


# =====================================================
# MEDICATION MANAGEMENT
# =====================================================

elif page == "Medications":

    st.title("💊 Medication Management")
    st.write("Organise medication information in one place.")

    with st.container(border=True):

        st.subheader("➕ Add a Medication")

        with st.form("medication_form"):

            medicine_name = st.text_input("Medication name")
            scheduled_time = st.text_input("Scheduled time")
            notes = st.text_area("Additional notes")

            add_medicine = st.form_submit_button(
                "Add Medication",
                use_container_width=True
            )

        if add_medicine:

            if not medicine_name.strip():
                st.warning("Enter a medication name.")

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
                    st.success("Medication added successfully!")
                    st.rerun()

    st.divider()

    st.subheader("Your Medication Records")

    medications = get_data("Medications")

    if medications:

        for med in medications:

            with st.container(border=True):

                st.markdown(
                    f"### 💊 {med.get('name', 'Medication')}"
                )

                st.write(
                    f"**Scheduled time:** {med.get('scheduled_time', 'Not set')}"
                )

                st.write(
                    f"**Notes:** {med.get('notes', '')}"
                )

                current_status = med.get("status", "Pending")

                options = ["Pending", "Recorded"]

                if current_status not in options:
                    current_status = "Pending"

                selected_status = st.selectbox(
                    "Medication status",
                    options,
                    index=options.index(current_status),
                    key=f"status_{med.get('id')}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Save Status",
                        key=f"save_{med.get('id')}",
                        use_container_width=True
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
                        key=f"delete_{med.get('id')}",
                        use_container_width=True
                    ):

                        if delete_data(
                            "Medications",
                            med.get("id")
                        ):
                            st.success("Medication deleted.")
                            st.rerun()

    else:
        st.info("No medication records found.")


# =====================================================
# APPOINTMENTS
# =====================================================

elif page == "Appointments":

    st.title("📅 Appointment Manager")
    st.write("Keep important appointments organised.")

    with st.container(border=True):

        st.subheader("➕ Create an Appointment")

        with st.form("appointment_form"):

            title = st.text_input("Appointment title")

            appointment_date = st.date_input(
                "Appointment date",
                value=date.today()
            )

            appointment_time = st.text_input("Appointment time")
            details = st.text_area("Appointment details")

            add_appointment = st.form_submit_button(
                "Add Appointment",
                use_container_width=True
            )

        if add_appointment:

            if not title.strip():
                st.warning("Enter an appointment title.")

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

    if appointments:

        for appointment in appointments:

            with st.container(border=True):

                st.markdown(
                    f"### 📅 {appointment.get('title', 'Appointment')}"
                )

                st.write(
                    f"**Date:** {appointment.get('date', '')}"
                )

                st.write(
                    f"**Time:** {appointment.get('time', '')}"
                )

                st.write(
                    f"**Details:** {appointment.get('details', '')}"
                )

                if st.button(
                    "Delete Appointment",
                    key=f"delete_app_{appointment.get('id')}"
                ):

                    if delete_data(
                        "appoinments",
                        appointment.get("id")
                    ):
                        st.success("Appointment deleted.")
                        st.rerun()

    else:
        st.info("No appointments have been added.")


# =====================================================
# CARE CIRCLE
# =====================================================

elif page == "Care Circle":

    st.title("👥 Your Care Circle")
    st.write("Bring your care network together.")

    with st.container(border=True):

        st.subheader("➕ Add a Member")

        with st.form("member_form"):

            member_name = st.text_input("Member name")

            add_member = st.form_submit_button(
                "Add Member",
                use_container_width=True
            )

        if add_member:

            if not member_name.strip():
                st.warning("Enter a member name.")

            else:

                success = add_data(
                    "Members",
                    {
                        "name": member_name.strip()
                    }
                )

                if success:
                    st.success("Member added!")
                    st.rerun()

    st.divider()

    st.subheader("Your Care Network")

    members = get_data("Members")

    if members:

        member_columns = st.columns(2)

        for index, member in enumerate(members):

            with member_columns[index % 2]:

                with st.container(border=True):

                    st.markdown("## 👤")
                    st.write(
                        f"**{member.get('name', 'Member')}**"
                    )

                    if st.button(
                        "Remove Member",
                        key=f"remove_{member.get('id')}"
                    ):

                        if delete_data(
                            "Members",
                            member.get("id")
                        ):
                            st.success("Member removed.")
                            st.rerun()

    else:
        st.info("Your Care Circle is currently empty.")


# =====================================================
# ACTIVITY FEED
# =====================================================

elif page == "Activity Feed":

    st.title("📋 Activity Feed")

    st.write(
        "An overview of the records currently saved in CareCircle."
    )

    st.subheader("💊 Medication Records")

    if medications:

        for med in reversed(medications):

            with st.container(border=True):

                st.write(
                    f"**{med.get('name', 'Medication')}**"
                )

                st.write(
                    f"Status: {med.get('status', 'Pending')}"
                )

                st.write(
                    f"Time: {med.get('scheduled_time', 'Not set')}"
                )

    else:
        st.info("No medication activity yet.")

    st.divider()

    st.subheader("📅 Appointment Records")

    if appointments:

        for appointment in reversed(appointments):

            with st.container(border=True):

                st.write(
                    f"**{appointment.get('title', 'Appointment')}**"
                )

                st.write(
                    f"Date: {appointment.get('date', '')}"
                )

                st.write(
                    f"Time: {appointment.get('time', '')}"
                )

    else:
        st.info("No appointment activity yet.")

    st.divider()

    st.subheader("👥 Care Circle Updates")

    if members:

        for member in reversed(members):

            with st.container(border=True):

                st.write(
                    f"👤 **{member.get('name', 'Member')}**"
                )

    else:
        st.info("No Care Circle members yet.")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:15px;">
    <h3 style="color:#16834b !important;">
        💚 CareCircle
    </h3>
    <p>
        Care better. Stay connected.
    </p>
    <p style="font-size:12px;color:#718579;">
        Hackathon Demonstration Project |
        Everyday Care Coordination
    </p>
    <p style="font-size:11px;color:#718579;">
        Not a medical or clinical system.
        Medication records are user-reported.
    </p>
</div>
""", unsafe_allow_html=True)
