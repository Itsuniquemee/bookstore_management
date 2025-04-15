def get_all_genres(db):
    return list(db.genres.find())

def add_genre(db, genre_data):
    db.genres.insert_one(genre_data)
