# app.py - Main Application
import streamlit as st
from routes.user_portal import show as show_user_portal
from routes.seller_portal import show as show_seller_portal
from routes import user_portal, seller_portal, admin_portal
from utils.auth import initialize_session
import bcrypt

# App Configuration
st.set_page_config(
    page_title="📚 BookSphere Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
initialize_session()

# Custom CSS
def inject_css():
    st.markdown("""
    <style>
        .main {padding: 2rem 3rem;}
        .sidebar .sidebar-content {background: #f8f9fa;}
        .stButton>button {border-radius: 8px; padding: 0.5rem 1rem;}
        .stTextInput>div>div>input {border-radius: 8px;}
        .book-card {border: 1px solid #ddd; border-radius: 10px; padding: 1.5rem; margin-bottom: 1rem;}
        .feedback-form {background: #f8f9fa; padding: 1.5rem; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# Hardcoded credentials (username: password)
HARDCODED_USERS = {
    "user1": {"password": "userpass", "role": "user"},
    "seller1": {"password": "sellerpass", "role": "seller"},
    "admin": {"password": "admin123", "role": "admin"}
}

# Authentication Logic
def authenticate(username, password, role):
    user = HARDCODED_USERS.get(username)
    if user and user["password"] == password and user["role"] == role:
        return True
    return False

# Authentication Portal
def show_auth():
    st.title("🔐 BookSphere Login")
    with st.form("login_form"):
        role = st.selectbox("Role", ["User", "Seller", "Admin"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            if authenticate(username, password, role.lower()):
                st.session_state.authenticated = True
                st.session_state.role = role.lower()
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials or role mismatch.")

# Main App Logic
def main():
    if not st.session_state.get('authenticated'):
        show_auth()
    else:
        with st.sidebar:
            st.title(f"Welcome, {st.session_state.username}!")
            st.write(f"Role: {st.session_state.role.capitalize()}")

            if st.button("🚪 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

            if st.session_state.role == "admin":
                st.page_link("admin_portal.py", label="Admin Dashboard", icon="🛡️")

            st.divider()
            st.write("BookSphere v1.0")

        # Role-based views
        if st.session_state.role == "user":
            user_portal.show()
        elif st.session_state.role == "seller":
            seller_portal.show()
        elif st.session_state.role == "admin":
            admin_portal.show()

if __name__ == "__main__":
    main()
