def get_all_customers(db):
    return list(db.customers.find())

def add_customer(db, customer_data):
    db.customers.insert_one(customer_data)
