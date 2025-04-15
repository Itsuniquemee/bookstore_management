def get_all_authors(db):
    return list(db.authors.find())

def add_author(db, author_data):
    db.authors.insert_one(author_data)
