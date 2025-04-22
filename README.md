# Bookstore Inventory Management System

## Overview

A Flask-based REST API for managing bookstore inventory, sales, and customer data using MongoDB as the database backend.

## Features

- **Inventory Management**:
  - Track books, authors, and genres
  - Automatic stock level monitoring
  - Low stock alerts
- **Sales Processing**:
  - Record sales transactions
  - Automatic inventory updates
  - Sales reporting
- **Customer Management**:
  - Customer profiles
  - Purchase history tracking
  - Top customers identification

## Technologies Used

- Python 3.9+
- Flask 2.3.2
- MongoDB 5.0+
- PyMongo 4.3.3
- Flask-PyMongo 2.3.0

## Installation

1. **Prerequisites**:
   - Python 3.9 or higher
   - MongoDB server running locally or accessible

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/bookstore-inventory.git
   cd bookstore-inventory
   ```

3. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration**:
   Create a `.env` file in the root directory with the following content:
   ```
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=bookstore_inventory
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=jwt-secret-key-here
   DEBUG=True
   ```

## Running the Application

Start the development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Inventory Management
- `GET /api/inventory/books` - List all books
- `POST /api/inventory/books` - Add new book
- `PUT /api/inventory/books/<book_id>` - Update book
- `GET /api/inventory/books/low-stock` - Get low stock books

### Sales
- `POST /api/sales/` - Record new sale
- `GET /api/sales/report` - Generate sales report

### Customers
- `POST /api/customers/` - Add new customer
- `GET /api/customers/<customer_id>` - Get customer details
- `GET /api/customers/top` - Get top customers

## Testing

Run tests using pytest:
```bash
pytest tests/
```

## Project Structure

```
bookstore_inventory/
├── app.py                      # Main application
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
│
├── models/                     # Data models
│   ├── __init__.py
│   ├── book.py
│   ├── author.py
│   ├── genre.py
│   ├── sale.py
│   └── customer.py
│
├── routes/                     # API routes
│   ├── __init__.py
│   ├── inventory.py
│   ├── sales.py
│   └── customers.py
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── database.py
│   ├── helpers.py
│   └── validators.py
│
└── tests/                      # Tests
    ├── __init__.py
    ├── test_models.py
    └── test_routes.py
```

## License

This project is licensed under https://github.com/Itsuniquemee/bookstore_management
