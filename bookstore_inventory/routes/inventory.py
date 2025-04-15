import streamlit as st
from utils.database import get_db
from models import book

def show():
    db = get_db()
    st.subheader("📦 Inventory Management")

    books = book.get_all_books(db)
    for b in books:
        st.write(f"{b.get('title')} by {b.get('author')}")

    if st.button("Add Sample Book"):
        book.add_book(db, {"title": "Sample Book", "author": "Jane Doe", "genre": "Fiction"})
