# models/feedback.py - Feedback Model
from utils.database import get_db
from datetime import datetime
from bson.objectid import ObjectId

def submit_feedback(db, feedback_data):
    """Submit user feedback to the database"""
    try:
        feedback_data["submitted_at"] = datetime.now()
        result = db.feedback.insert_one(feedback_data)
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        return False

def get_all_feedback(db, limit=100):
    """Retrieve all feedback entries"""
    return list(db.feedback.find().sort("submitted_at", -1).limit(limit))

def get_feedback_by_user(db, username):
    """Get feedback submitted by a specific user"""
    return list(db.feedback.find({"user": username}).sort("submitted_at", -1))

def get_feedback_by_type(db, feedback_type):
    """Filter feedback by type (suggestion, bug report, etc.)"""
    return list(db.feedback.find({"type": feedback_type}).sort("submitted_at", -1))

def calculate_average_rating(db):
    """Calculate the average feedback rating"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "averageRating": {"$avg": "$rating"},
                "count": {"$sum": 1}
            }
        }
    ]
    result = list(db.feedback.aggregate(pipeline))
    return result[0] if result else {"averageRating": 0, "count": 0}

def resolve_feedback(db, feedback_id, resolution_notes):
    """Mark feedback as resolved with admin notes"""
    try:
        result = db.feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {
                "$set": {
                    "resolved": True,
                    "resolved_at": datetime.now(),
                    "resolution_notes": resolution_notes
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error resolving feedback: {e}")
        return False