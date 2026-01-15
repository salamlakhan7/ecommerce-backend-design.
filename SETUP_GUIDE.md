# Running the E-Commerce Project with Django Backend

## Project Structure

```
Ecommerce-website/
├── Frontend/ (HTML, CSS, JavaScript files)
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── ...
├── backend/ (Django)
│   ├── manage.py
│   ├── requirements.txt
│   ├── ecommerce_project/ (Django settings)
│   └── ecommerce/ (Django app)
```

## Setup Instructions

### 1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH"

### 2. **Create Virtual Environment** (Optional but Recommended)

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (Windows)
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Database Setup**

```bash
# Run migrations
python manage.py migrate

# Create superuser (for admin panel)
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### 5. **Load Sample Data (Optional)**

```bash
python manage.py loaddata sample_products
```

### 6. **Run Django Server**

```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

**API Endpoints:**
- Products: `http://localhost:8000/api/products/`
- Categories: `http://localhost:8000/api/categories/`
- Cart: `http://localhost:8000/api/carts/`
- Orders: `http://localhost:8000/api/orders/`
- Admin: `http://localhost:8000/admin/`

### 7. **Run Frontend** (In a separate terminal)

```bash
# Navigate to the frontend directory (root of the project)
cd ..

# If you have Python SimpleServer or any local server
python -m http.server 3000
```

Or use any other local server (VS Code Live Server extension, Node.js http-server, etc.)

## API Documentation

### Products
- **GET** `/api/products/` - List all products
- **GET** `/api/products/{id}/` - Get product details
- **GET** `/api/products/?category=electronics` - Filter by category
- **GET** `/api/products/?search=laptop` - Search products

### Cart
- **GET** `/api/carts/my-cart/?session_id=YOUR_SESSION_ID` - Get current cart
- **POST** `/api/carts/add-item/` - Add item to cart
  ```json
  {
    "product_id": 1,
    "quantity": 2,
    "session_id": "YOUR_SESSION_ID"
  }
  ```
- **POST** `/api/carts/update-item/` - Update cart item
  ```json
  {
    "cart_item_id": 1,
    "quantity": 3,
    "session_id": "YOUR_SESSION_ID"
  }
  ```
- **POST** `/api/carts/remove-item/` - Remove from cart
  ```json
  {
    "cart_item_id": 1,
    "session_id": "YOUR_SESSION_ID"
  }
  ```
- **POST** `/api/carts/clear/` - Clear entire cart

### Orders
- **POST** `/api/orders/` - Create a new order
  ```json
  {
    "session_id": "YOUR_SESSION_ID",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "city": "New York",
    "country": "USA",
    "zip_code": "10001",
    "payment_method": "card"
  }
  ```
- **GET** `/api/orders/?session_id=YOUR_SESSION_ID` - Get orders by session

## Frontend Integration

Update your JavaScript files to make API calls to the Django backend:

```javascript
// Example API call
fetch('http://localhost:8000/api/products/')
  .then(response => response.json())
  .then(data => {
    // Handle products data
    console.log(data);
  });
```

## Next Steps

1. **Populate Database:** Add products through the Django admin panel or create a fixture file
2. **Update Frontend:** Modify `script.js` and other JS files to call the Django API endpoints
3. **Implement Authentication:** Add user login/registration if needed
4. **Deploy:** Use platforms like Heroku, PythonAnywhere, or AWS for production

## Troubleshooting

**Port 8000 already in use:**
```bash
python manage.py runserver 8080
```

**CORS Issues:** Ensure `CORS_ALLOWED_ORIGINS` in `settings.py` includes your frontend URL

**Database Issues:**
```bash
# Delete db.sqlite3 and recreate
python manage.py migrate
```

## Support

For more information on Django REST Framework:
- https://www.django-rest-framework.org/
