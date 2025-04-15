# routes/seller_portal.py - Complete Seller Portal
import streamlit as st
import pandas as pd
from utils.database import get_db
from models.book import add_book, update_book, delete_book
from models.order import get_seller_orders
from datetime import datetime, timedelta

def show():
    db = get_db()
    
    st.title("📊 Seller Dashboard")
    st.write(f"Logged in as: {st.session_state.username}")
    
    # Performance metrics
    show_seller_metrics(db)
    
    # Tabbed interface
    inv_tab, orders_tab, reports_tab = st.tabs(["📦 Inventory", "📝 Orders", "📈 Reports"])
    
    with inv_tab:
        manage_inventory(db)
    
    with orders_tab:
        manage_orders(db)
    
    with reports_tab:
        generate_reports(db)

def show_seller_metrics(db):
    """Display key performance indicators"""
    today = datetime.now()
    last_week = today - timedelta(days=7)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_books = db.books.count_documents({"added_by": st.session_state.username})
        st.metric("Your Books", total_books)
    
    with col2:
        weekly_sales = db.orders.count_documents({
            "seller": st.session_state.username,
            "order_date": {"$gte": last_week}
        })
        st.metric("Weekly Orders", weekly_sales)
    
    with col3:
        result = db.orders.aggregate([
            {"$match": {
                "seller": st.session_state.username,
                "order_date": {"$gte": last_week}
            }},
            {"$group": {"_id": None, "total": {"$sum": "$price"}}}
        ])
        total = next(result, {}).get("total", 0)
        st.metric("Weekly Revenue", f"₹{total:.2f}")

def manage_inventory(db):
    """Inventory management system"""
    st.subheader("Manage Your Inventory")
    
    # Add new book form
    with st.expander("➕ Add New Book", expanded=False):
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*")
                author = st.text_input("Author*")
                isbn = st.text_input("ISBN")
            with col2:
                genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "History"])
                price = st.number_input("Price*", min_value=0.0, step=0.01)
                stock = st.number_input("Initial Stock", min_value=0, step=1)
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Add Book"):
                if not title or not author or price <= 0:
                    st.error("Please fill required fields (*)")
                else:
                    book_data = {
                        "title": title,
                        "author": author,
                        "isbn": isbn,
                        "genre": genre,
                        "price": price,
                        "stock": stock,
                        "description": description,
                        "added_by": st.session_state.username,
                        "added_on": datetime.now()
                    }
                    if add_book(db, book_data):
                        st.success("Book added successfully!")
                    else:
                        st.error("Failed to add book")
    
    # Edit existing books
    st.subheader("Current Inventory")
    books = list(db.books.find({"added_by": st.session_state.username}))
    
    if not books:
        st.info("No books in inventory yet")
    else:
        df = pd.DataFrame(books)
        edited_df = st.data_editor(
            df[['title', 'author', 'genre', 'price', 'stock']],
            num_rows="dynamic",
            use_container_width=True
        )
        
        if st.button("Save Changes"):
            for _, row in edited_df.iterrows():
                update_data = {
                    "price": row['price'],
                    "stock": row['stock']
                }
                update_book(db, row['title'], update_data)
            st.success("Inventory updated!")

def manage_orders(db):
    """Order management system with real-time updates"""
    st.subheader("Customer Orders")
    
    # Status filter
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "pending", "confirmed", "shipped", "delivered", "cancelled"],
        index=0
    )
    
    # Get orders with book details
    query = {"seller": st.session_state.username}
    if status_filter != "All":
        query["status"] = status_filter
    
    orders = list(db.orders.find(query).sort("order_date", -1))
    
    if not orders:
        st.info("No orders found")
        return
    
    for order in orders:
        with st.container(border=True):
            cols = st.columns([3, 1, 1, 1])
            cols[0].write(f"**{order['book_title']}**")
            cols[0].caption(f"Order #: {str(order['_id'])[-6:]} • {order['user']}")
            cols[1].write(f"₹{order['price']:.2f}")
            
            # Status display with color coding
            status_color = {
                'pending': 'orange',
                'confirmed': 'blue',
                'shipped': 'green',
                'delivered': 'darkgreen',
                'cancelled': 'red'
            }
            cols[2].markdown(
                f"<span style='color:{status_color.get(order['status'], 'black')}'>"
                f"**{order['status'].capitalize()}**</span>",
                unsafe_allow_html=True
            )
            
            # Status update dropdown
            if order['status'] not in ['delivered', 'cancelled']:
                new_status = cols[3].selectbox(
                    "Update status",
                    ["confirmed", "shipped", "delivered"],
                    key=f"status_{order['_id']}"
                )
                if cols[3].button("Update", key=f"btn_{order['_id']}"):
                    db.orders.update_one(
                        {"_id": order["_id"]},
                        {"$set": {"status": new_status, "updated_at": datetime.now()}}
                    )
                    st.success(f"Status updated to {new_status}!")
                    st.rerun()
            
            # Order details expander
            with st.expander("View details"):
                st.write(f"**Order Date:** {order['order_date'].strftime('%b %d, %Y %H:%M')}")
                if 'updated_at' in order:
                    st.write(f"**Last Updated:** {order['updated_at'].strftime('%b %d, %Y %H:%M')}")

def generate_reports(db):
    """Sales reporting system"""
    st.subheader("Sales Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Convert to datetime
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())
    
    # Get sales data
    orders = list(db.orders.find({
        "seller": st.session_state.username,
        "order_date": {"$gte": start_dt, "$lte": end_dt}
    }).sort("order_date", -1))
    
    if not orders:
        st.warning("No orders in selected period")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(orders)
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Display metrics
    total_sales = df['price'].sum()
    avg_order = total_sales / len(df)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Sales", f"₹{total_sales:.2f}")
    m2.metric("Total Orders", len(df))
    m3.metric("Avg Order Value", f"₹{avg_order:.2f}")
    
    # Sales trend chart
    st.subheader("Daily Sales Trend")
    daily_sales = df.set_index('order_date')['price'].resample('D').sum()
    st.line_chart(daily_sales)
    
    # Status distribution
    st.subheader("Order Status Distribution")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)