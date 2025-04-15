def record_sale(db, sale_data):
    db.sales.insert_one(sale_data)

def get_sales(db):
    return list(db.sales.find())
