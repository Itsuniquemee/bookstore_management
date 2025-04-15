# utils/auth.py - Authentication System
import bcrypt
import streamlit as st
from datetime import datetime
from utils.database import get_db

def initialize_session():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_time' not in st.session_state:
        st.session_state.current_time = datetime.now()

def authenticate_user(username, password, role):
    db = get_db()
    user = db.users.find_one({"username": username})
    if user:
        stored_pw = user["password"]
        if isinstance(stored_pw, str):
            stored_pw = stored_pw.encode('utf-8')  # encode string back to bytes for bcrypt check

        if bcrypt.checkpw(password.encode('utf-8'), stored_pw) and user['role'].lower() == role.lower():
            return True
    return False

def hash_password(password: str) -> bytes:
    """Generate password hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())