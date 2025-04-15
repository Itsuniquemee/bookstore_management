# models/book.py - Complete Book Model
from utils.database import get_db
from datetime import datetime
from bson.objectid import ObjectId

def get_all_books(db):
    """Get all books in the database"""
    return list(db.books.find())

def get_books(db, search_query="", genre_filter="All", price_range=(0, 100)):
    """
    Get filtered books based on search criteria
    Args:
        db: Database connection
        search_query: String to search in title/author
        genre_filter: Genre to filter by
        price_range: Tuple of (min_price, max_price)
    """
    query = {}
    
    # Add search query filter
    if search_query:
        query["$or"] = [
            {"title": {"$regex": search_query, "$options": "i"}},
            {"author": {"$regex": search_query, "$options": "i"}}
        ]
    
    # Add genre filter
    if genre_filter != "All":
        query["genre"] = genre_filter
    
    # Add price range filter
    query["price"] = {"$gte": price_range[0], "$lte": price_range[1]}
    
    return list(db.books.find(query).sort("title", 1))

def get_book_by_id(db, book_id):
    """Get a single book by its ID"""
    return db.books.find_one({"_id": ObjectId(book_id)})

def add_book(db, book_data):
    """Add a new book to the database"""
    try:
        result = db.books.insert_one(book_data)
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error adding book: {e}")
        return False

def update_book(db, book_title, update_data):
    """Update book information"""
    try:
        result = db.books.update_one(
            {"title": book_title},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating book: {e}")
        return False

def delete_book(db, book_id):
    """Remove a book from the database"""
    try:
        result = db.books.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting book: {e}")
        return False

def get_genres(db):
    """Get all unique genres in the system"""
    return db.books.distinct("genre")

def decrease_stock(db, book_id, quantity=1):
    """Decrease book stock when an order is placed"""
    try:
        result = db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$inc": {"stock": -quantity}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error decreasing stock: {e}")
        return False