from bson import ObjectId
from datetime import datetime

def validate_book_data(data):
    required_fields = ['title', 'isbn', 'price', 'quantity']
    if not all(field in data for field in required_fields):
        return False, "Missing required fields"
    
    try:
        float(data['price'])
        int(data['quantity'])
    except (ValueError, TypeError):
        return False, "Invalid price or quantity format"
    
    return True, ""

def validate_sale_data(data):
    required_fields = ['book_id', 'quantity', 'total_amount']
    if not all(field in data for field in required_fields):
        return False, "Missing required fields"
    
    try:
        ObjectId(data['book_id'])
        int(data['quantity'])
        float(data['total_amount'])
    except:
        return False, "Invalid data formats"
    
    return True, ""
