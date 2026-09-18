# 🚀 Coderr Backend REST API

<p align="center">
  <strong>A modular REST API for a modern service marketplace platform.</strong>
</p>

<p align="center">
  Built with Django 6.x · Django REST Framework · SQLite · Token Authentication
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.x-092E20?style=for-the-badge\&logo=django\&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST_API-A30000?style=for-the-badge)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

## ⚡ Quick Start (TL;DR)

Get the project up and running locally in 5 simple steps:

```bash
# 1. Clone the repository and navigate into the project
git clone https://github.com/<your-username>/coderr-backend.git
cd coderr-backend

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Configure environment variables (create .env file)
# Create a .env file containing:
# SECRET_KEY=your_django_secret_key_here
# DEBUG=True

# 5. Apply migrations and start development server
python manage.py migrate
python manage.py runserver
```

Server will be running at `http://127.0.0.1:8000/api/` 🎉

---

## ✨ About the Project


**Coderr** is a modular service marketplace backend built with **Django** and **Django REST Framework (DRF)**.

The API provides the complete backend infrastructure for a platform where businesses can publish service offers, customers can place orders, and users can interact through reviews and ratings.

The project is structured into independent Django applications, making the codebase easier to maintain, extend, and scale.

### 🎯 Core Concept

> **Businesses offer services. Customers place orders. Completed interactions can generate reviews and ratings.**

The backend handles the complete workflow from registration and authentication to offers, orders, reviews, and platform-wide statistics.

---

# 🛠 Tech Stack

| Technology                   | Purpose                       |
| ---------------------------- | ----------------------------- |
| 🐍 **Python 3.12+**          | Programming language          |
| 🟢 **Django 6.x**            | Backend framework             |
| 🔌 **Django REST Framework** | REST API                      |
| 🗄️ **SQLite**               | Development database          |
| 🔐 **Token Authentication**  | API authentication            |
| 🔎 **django-filter**         | API filtering                 |
| 🌐 **django-cors-headers**   | Cross-Origin Resource Sharing |

---

# 🧩 Project Architecture

Coderr is divided into several modular Django applications.

```text
coderr-backend/
│
├── auth_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── offers_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── orders_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── reviews_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# 📦 Features

## 🔐 Authentication & Profiles

The `auth_app` manages users and profiles.

### Features

* User registration
* Login with token authentication
* Business accounts
* Customer accounts
* Profile management
* Business profile listing
* Customer profile listing

---

## 💼 Service Offers

The `offers_app` manages services offered by businesses.

Each offer follows a strict **three-tier package system**:

```text
┌─────────────┐
│    BASIC    │
├─────────────┤
│  STANDARD   │
├─────────────┤
│   PREMIUM   │
└─────────────┘
```

### Features

* Create service offers
* Update own offers
* Delete own offers
* Retrieve individual offers
* Three required packages
* Offer detail endpoints
* Aggregated platform statistics

---

## 📦 Orders

The `orders_app` handles the complete order workflow.

### Order Statuses

```text
        ┌──────────────┐
        │ IN_PROGRESS  │
        └──────┬───────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│  COMPLETED  │  │  CANCELLED  │
└─────────────┘  └─────────────┘
```

### Features

* Create orders
* View user orders
* Update order status
* Cancel orders
* Complete orders
* Count active business orders
* Count completed business orders

---

## ⭐ Reviews & Ratings

The `reviews_app` provides the rating and feedback system.

### Features

* View reviews
* Create reviews
* Update own reviews
* Delete own reviews
* Customer-only review creation
* Validation of authentic interactions
* Rating aggregation

---

# 📊 Platform Statistics

Coderr provides aggregated platform information through:

```http
GET /api/base-info/
```

Example response:

```json
{
  "review_count": 120,
  "average_rating": 4.7,
  "offer_count": 35
}
```

---

# 🚀 Getting Started

Follow the steps below to run the backend locally.

## 1️⃣ Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/<your-username>/coderr-backend.git
```

Then enter the project directory:

```bash
cd coderr-backend
```

> 💡 Replace `<your-username>` with your GitHub username.

---

## 2️⃣ Create a Virtual Environment

A virtual environment keeps the project's dependencies isolated from your global Python installation.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
.\venv\Scripts\activate
```

If you are using PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

After activation, you should see something similar to:

```text
(venv) C:\...\coderr-backend>
```

---

## 3️⃣ Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root, next to `manage.py`.

```text
coderr-backend/
├── .env
├── manage.py
├── requirements.txt
└── ...
```

Add:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

### 🔒 Important

Never commit your real secret key to GitHub.

Make sure `.env` is included in your `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 5️⃣ Create Database Migrations

Run:

```bash
python manage.py makemigrations
```

Then apply the migrations:

```bash
python manage.py migrate
```

This creates the required database tables.

---

## 6️⃣ Create a Superuser

Create an administrator account:

```bash
python manage.py createsuperuser
```

Django will ask you for:

```text
Username:
Email address:
Password:
Password (again):
```

The account can then be used to access the Django Admin interface.

---

## 7️⃣ Start the Development Server

Run:

```bash
python manage.py runserver
```

You should see something similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

Your backend is now running 🎉

### 🌐 API

```text
http://127.0.0.1:8000/api/
```

### 🛠 Django Admin

```text
http://127.0.0.1:8000/admin/
```

---

# 📡 API Documentation

All API endpoints use the `/api/` prefix.

---

## 🔐 Authentication & Profiles

| Method  | Endpoint                  | Description                     | Authentication |
| ------- | ------------------------- | ------------------------------- | -------------- |
| `POST`  | `/api/registration/`      | Register a business or customer | ❌              |
| `POST`  | `/api/login/`             | Login and receive token         | ❌              |
| `GET`   | `/api/profile/<id>/`      | View profile                    | 🔐 Owner       |
| `PATCH` | `/api/profile/<id>/`      | Update profile                  | 🔐 Owner       |
| `GET`   | `/api/profiles/business/` | List businesses                 | ❌              |
| `GET`   | `/api/profiles/customer/` | List customers                  | ❌              |

---

## 💼 Offers

| Method   | Endpoint                  | Description           | Authentication |
| -------- | ------------------------- | --------------------- | -------------- |
| `GET`    | `/api/offers/`            | List all offers       | ❌              |
| `POST`   | `/api/offers/`            | Create an offer       | 🔐 Business    |
| `GET`    | `/api/offers/<id>/`       | Retrieve an offer     | ❌              |
| `PATCH`  | `/api/offers/<id>/`       | Update an offer       | 🔐 Owner       |
| `DELETE` | `/api/offers/<id>/`       | Delete an offer       | 🔐 Owner       |
| `GET`    | `/api/offerdetails/<id>/` | Retrieve tier details | ❌              |

---

## 📦 Orders

| Method   | Endpoint                                         | Description            | Authentication |
| -------- | ------------------------------------------------ | ---------------------- | -------------- |
| `GET`    | `/api/orders/`                                   | List user orders       | 🔐             |
| `POST`   | `/api/orders/`                                   | Create an order        | 🔐             |
| `PATCH`  | `/api/orders/<id>/`                              | Update order status    | 🔐             |
| `DELETE` | `/api/orders/<id>/`                              | Delete an order        | 🔐             |
| `GET`    | `/api/order-count/<business_user_id>/`           | Count active orders    | ❌              |
| `GET`    | `/api/completed-order-count/<business_user_id>/` | Count completed orders | ❌              |

### Available Order Statuses

```text
in_progress
completed
cancelled
```

---

## ⭐ Reviews & Platform Metrics

| Method   | Endpoint             | Description         | Authentication |
| -------- | -------------------- | ------------------- | -------------- |
| `GET`    | `/api/reviews/`      | List reviews        | ❌              |
| `POST`   | `/api/reviews/`      | Create a review     | 🔐 Customer    |
| `PATCH`  | `/api/reviews/<id>/` | Update own review   | 🔐 Owner       |
| `DELETE` | `/api/reviews/<id>/` | Delete own review   | 🔐 Owner       |
| `GET`    | `/api/base-info/`    | Platform statistics | ❌              |

---

# 🔑 Authentication

Protected endpoints require a token in the HTTP request header.

```http
Authorization: Token <your_token_here>
```

### Example

```http
GET /api/orders/
Authorization: Token 123456789abcdef
```

---

# 🧪 Example API Workflow

A typical customer workflow could look like this:

```text
┌──────────────────┐
│  Register User   │
└────────┬─────────┘
         ▼
┌──────────────────┐
│      Login       │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Browse Services  │
└────────┬─────────┘
         ▼
┌──────────────────┐
│   Place Order    │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Complete Order   │
└────────┬─────────┘
         ▼
┌──────────────────┐
│   Leave Review   │
└──────────────────┘
```

A business workflow:

```text
Register
   │
   ▼
Create Profile
   │
   ▼
Create Service Offer
   │
   ▼
Receive Orders
   │
   ▼
Process Orders
   │
   ▼
Complete Orders
   │
   ▼
Receive Customer Reviews
```

---

# 🛡️ Security

The API uses Django REST Framework's token authentication system.

Protected resources require:

```http
Authorization: Token <token>
```

Sensitive environment configuration should be stored in `.env` and excluded from version control.

---

# 🧑‍💻 Development

Start the server with:

```bash
python manage.py runserver
```

Create migrations after model changes:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

---

# 📁 Recommended `.gitignore`

Make sure your repository does not contain local or sensitive files:

```gitignore
# Environment
.env

# Virtual environment
venv/
env/

# Python
__pycache__/
*.py[cod]

# Django
db.sqlite3
media/
staticfiles/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

# 🎨 API Design Philosophy

Coderr follows a modular backend architecture with a clear separation of responsibilities.

### 🔹 Authentication

Handles:

* Users
* Profiles
* Login
* Registration
* Permissions

### 🔹 Offers

Handles:

* Services
* Packages
* Pricing
* Offer details

### 🔹 Orders

Handles:

* Purchases
* Order lifecycle
* Business workload
* Completion tracking

### 🔹 Reviews

Handles:

* Ratings
* Feedback
* Review validation
* Platform statistics

This separation keeps the backend maintainable and makes future features easier to add.

---

# 🔮 Possible Future Improvements

Some potential extensions include:

* 🐘 PostgreSQL for production
* 🐳 Docker support
* 📖 Swagger / OpenAPI documentation
* 🧪 Automated API tests
* 🔄 CI/CD pipeline
* ☁️ Cloud deployment
* 🔐 JWT authentication
* 📧 Email notifications
* 🔔 Real-time notifications
* 💳 Payment integration
* 📈 Advanced analytics

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

### Typical workflow

```bash
git checkout -b feature/my-feature
```

Make your changes and commit them:

```bash
git add .
git commit -m "Add my feature"
```

Push your branch:

```bash
git push origin feature/my-feature
```

Then open a Pull Request on GitHub.

---

# 📄 License

This project is available under the **MIT License**.

---

# 👨‍💻 Author

**Your Name**

Backend Developer · Django · REST APIs · Python

<p align="center">

⭐ If you like this project, consider giving it a star on GitHub!

</p>
