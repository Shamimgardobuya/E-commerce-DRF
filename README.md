# 🛒 E-Commerce API

A simple yet robust **E-commerce backend** built with **Django REST Framework**.
The project provides APIs to manage customers, categories, products, and orders, forming the foundation for any online store.

---

## 🚀 Features

* **Authentication & Authorization**

  * Token-based authentication (e.g., JWT or OAuth2 ready)
  * Secure API endpoints with scope/permission checks

* **Customer Management**

  * Create and manage customer profiles

* **Category & Product Management**

  * Nested categories support
  * Product CRUD operations
  * Attach categories to products

* **Order Handling**

  * Place orders with multiple items
  * Track order details (status, customer, products, quantities)
  * Order update & retrieval APIs

* **Validation & Error Handling**

  * Consistent JSON responses
  * Serializer-based validation

* **Extensible Design**

  * Clean modular structure
  * Easily integrable with front-end apps or mobile clients

---

## 🏗️ Project Structure

```
ecommerce-api/
│── registration/       # Customer models, serializers, views
│── categories/      # Category models, serializers, views
│── products/        # Product models, serializers, views
│── orders/          # Orders & order items
│── ecommerce/       # Main project settings & urls
│── tests/           # Unit & integration tests
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

API will be available at:
👉 `pending`

---

## 📡 API Endpoints (Examples)

| Method | Endpoint               | Description       |
| ------ | ---------------------- | ----------------- |
| POST   | `register/`      | Create customer   |
| POST   | `/api/categories/`     | Create category   |
| GET    | `/api/products/`       | List products     |
| POST   | `/api/orders/`         | Place new order   |
| GET    | `/api/orders/{id}/`    | Get order details |

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL (or SQLite for development)
* **Auth:** JWT / OAuth2 (pluggable)
* **Other Tools:** Django Admin, Pytest/Unittest for testing

---



## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

Would you like me to also **add usage examples with cURL/Postman requests** for your main endpoints (like creating a product or placing an order)? That usually makes the README more practical for developers.
