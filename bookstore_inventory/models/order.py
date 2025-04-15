# models/order.py - Order Model
from utils.database import get_db
from datetime import datetime
from bson.objectid import ObjectId
from models.book import decrease_stock

def create_order(db, order_data):
    """Create a new order in the database"""
    try:
        # Decrease book stock first
        if not decrease_stock(db, order_data["book_id"]):
            return False
            
        order_data["created_at"] = datetime.now()
        order_data["status"] = "pending"  # Default status
        result = db.orders.insert_one(order_data)
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error creating order: {e}")
        return False

def get_order_by_id(db, order_id):
    """Get a single order by its ID"""
    return db.orders.find_one({"_id": ObjectId(order_id)})

def get_user_orders(db, username):
    """Get all orders for a specific user"""
    return list(db.orders.find({"username": username}).sort("created_at", -1))

def get_seller_orders(db, seller_username):
    """Get all orders for books added by a specific seller"""
    pipeline = [
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book_details"
            }
        },
        {"$unwind": "$book_details"},
        {
            "$match": {
                "book_details.added_by": seller_username
            }
        },
        {
            "$addFields": {
                "book_title": "$book_details.title"
            }
        }
    ]
    return list(db.orders.aggregate(pipeline))

def update_order_status(db, order_id, new_status):
    """Update the status of an order"""
    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        return False
        
    try:
        result = db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": new_status, "updated_at": datetime.now()}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating order status: {e}")
        return False

def cancel_order(db, order_id):
    """Cancel an order and restore stock"""
    try:
        # First get the order details
        order = get_order_by_id(db, order_id)
        if not order:
            return False
            
        # Restore the book stock
        db.books.update_one(
            {"_id": ObjectId(order["book_id"])},
            {"$inc": {"stock": 1}}
        )
        
        # Update order status
        return update_order_status(db, order_id, "cancelled")
    except Exception as e:
        print(f"Error cancelling order: {e}")
        return False