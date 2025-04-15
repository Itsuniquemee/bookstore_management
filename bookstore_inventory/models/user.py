import bcrypt

def create_user(db, username, password, role):
    hashed_pw = bcrypt.hashpw(password if isinstance(password, bytes) else password.encode(), bcrypt.gensalt())
    db.users.insert_one({
        "username": username,
        "password": hashed_pw,
        "role": role
    })
