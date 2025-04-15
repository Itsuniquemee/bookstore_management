import streamlit as st
from utils.database import get_db
from models import customer

def show():
    db = get_db()
    st.subheader("👥 Customer Management")

    customers = customer.get_all_customers(db)
    for c in customers:
        st.write(f"{c.get('name')} - {c.get('email')}")

    if st.button("Add Sample Customer"):
        customer.add_customer(db, {"name": "John Smith", "email": "john@example.com"})
