import streamlit as st
from utils.database import get_db
from models import sale

def show():
    db = get_db()
    st.subheader("💰 Sales Report")

    sales_data = sale.get_sales(db)
    for s in sales_data:
        st.write(f"Sold '{s.get('book')}' to {s.get('customer')} for ${s.get('price')}")
