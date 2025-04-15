# routes/user_portal.py - Updated with fixed order display
import streamlit as st
from utils.database import get_db
from models.book import get_all_books, get_book_by_id, get_genres
from models.order import create_order, get_user_orders, cancel_order
from models.feedback import submit_feedback
from datetime import datetime

def show():
    db = get_db()

    # Initialize cart session state
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # Header
    st.title("📚 BookSphere Reader Portal")
    st.write(f"Welcome back, {st.session_state.username}!")

    # Tabs
    browse_tab, cart_tab, orders_tab, feedback_tab = st.tabs([
        "🔍 Browse Books", "🛒 My Cart", "📦 My Orders", "💬 Feedback"
    ])

    with browse_tab:
        st.subheader("Discover Your Next Read")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("Search by title/author")
        with col2:
            genre_filter = st.selectbox("Genre", ["All"] + list(get_genres(db)))
        with col3:
            price_range = st.slider("Price Range", 0, 1000, (0, 1000))

        books = get_all_books(db)
        filtered_books = [
            b for b in books
            if (not search_query or search_query.lower() in b['title'].lower() or 
                search_query.lower() in b['author'].lower())
            and (genre_filter == "All" or b['genre'] == genre_filter)
            and (price_range[0] <= b['price'] <= price_range[1])
        ]

        if not filtered_books:
            st.info("No books found matching your criteria")
        else:
            for book in filtered_books:
                display_book_card(book)

    with cart_tab:
        show_cart(db)

    with orders_tab:
        show_order_history(db)

    with feedback_tab:
        show_feedback_form(db)

def display_book_card(book):
    """Display book card with Add to Cart button"""
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(book['title'])
            st.caption(f"by {book['author']} | {book['genre']} | Seller: {book.get('added_by', 'Unknown')}")
            st.write(book.get('description', 'No description available'))
            st.write(f"**Price:** ₹{book['price']:.2f}")
            st.write(f"**Stock:** {book.get('stock', 0)} available")

        with col2:
            if book.get('stock', 0) > 0:
                if st.button("🛒 Add to Cart", key=f"add_{book['_id']}"):
                    st.session_state.cart.append({
                        "book_id": book["_id"],
                        "book_title": book["title"],
                        "price": book["price"],
                        "seller": book.get("added_by", "unknown"),
                    })
                    st.success("Added to cart!")
                    st.rerun()
            else:
                st.warning("Out of stock")

def show_cart(db):
    """Show books added to cart and allow placing order"""
    st.subheader("Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        return

    total = 0
    for idx, item in enumerate(st.session_state.cart):
        book = get_book_by_id(db, item["book_id"])
        if not book:
            continue
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{book['title']}** by {book['author']}")
            col1.write(f"₹{item['price']:.2f}")
            col2.button("❌ Remove", key=f"remove_{idx}", on_click=remove_from_cart, args=(idx,))
            total += item["price"]

    st.write(f"**Total:** ₹{total:.2f}")

    if st.button("✅ Place Order"):
        now = datetime.now()
        order_ids = []
        for item in st.session_state.cart:
            order_data = {
                "book_id": item["book_id"],
                "book_title": item["book_title"],
                "user": st.session_state.username,
                "seller": item["seller"],
                "price": item["price"],
                "status": "pending",
                "order_date": now
            }
            order_id = create_order(db, order_data)
            if order_id:
                order_ids.append(order_id)
                # Update book stock
                db.books.update_one(
                    {"_id": item["book_id"]},
                    {"$inc": {"stock": -1}}
                )

        if len(order_ids) == len(st.session_state.cart):
            st.success("All orders placed successfully!")
            st.session_state.cart.clear()
            st.rerun()
        elif order_ids:
            st.warning(f"Placed {len(order_ids)}/{len(st.session_state.cart)} orders")
        else:
            st.error("Failed to place any orders")

def remove_from_cart(index):
    """Remove item from cart by index"""
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)
        st.rerun()

def show_order_history(db):
    """Display user's orders in a tabular format"""
    st.subheader("Your Order History")
    
    # Get all orders for the current user
    orders = list(db.orders.find({"user": st.session_state.username}).sort("order_date", -1))
    
    if not orders:
        st.info("You haven't placed any orders yet")
        return
    
    # Create a list of dictionaries for the table data
    table_data = []
    for order in orders:
        # Format the dates
        order_date = order['order_date'].strftime('%Y-%m-%d %H:%M:%S') if 'order_date' in order else "N/A"
        updated_at = order.get('updated_at', order['order_date']).strftime('%Y-%m-%d %H:%M:%S')
        
        table_data.append({
            "Order ID": str(order['_id'])[-6:],
            "Book Title": order.get('book_title', 'Unknown'),
            "Price": f"₹{order['price']:.2f}",
            "Status": order['status'].capitalize(),
            "Seller": order.get('seller', 'Unknown'),
            "Order Date": order_date,
            "Last Updated": updated_at,
            "Contact Email": order.get('contact_email', 'N/A')
        })
    
    # Display the table
    st.dataframe(
        table_data,
        column_config={
            "Order ID": "Order ID",
            "Book Title": "Book",
            "Price": st.column_config.NumberColumn("Price (₹)"),
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
            ),
            "Seller": "Seller",
            "Order Date": "Order Date",
            "Last Updated": "Last Updated",
            "Contact Email": "Contact Email"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Add status filter
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "pending", "confirmed", "shipped", "delivered", "cancelled"],
        index=0,
        key="order_status_filter"
    )
    
    # Display filtered orders
    if status_filter != "All":
        filtered_orders = [order for order in table_data if order['Status'].lower() == status_filter]
        if not filtered_orders:
            st.info(f"No {status_filter} orders found")
        else:
            st.write(f"Showing {len(filtered_orders)} {status_filter} orders:")
            st.dataframe(filtered_orders, use_container_width=True, hide_index=True)
    
    # Debug option to show raw data
    if st.checkbox("Show raw orders data"):
        st.write("Raw orders data:", orders)

def show_feedback_form(db):
    """Interactive feedback form"""
    st.subheader("Share Your Thoughts")

    with st.form("feedback_form", clear_on_submit=True):
        feedback_type = st.selectbox("Feedback Type", 
                                   ["Suggestion", "Bug Report", "Compliment", "Other"])
        message = st.text_area("Your Message", 
                             placeholder="Please provide detailed feedback...", 
                             height=150)
        rating = st.slider("Rating (1-5)", 1, 5, 3)

        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            if len(message.strip()) < 10:
                st.error("Please provide at least 10 characters of feedback")
            else:
                feedback_data = {
                    "user": st.session_state.username,
                    "type": feedback_type,
                    "message": message.strip(),
                    "rating": rating,
                    "date": datetime.now(),
                    "status": "new"
                }
                if submit_feedback(db, feedback_data):
                    st.success("Thank you for your feedback!")
                else:
                    st.error("Failed to submit feedback. Please try again.")