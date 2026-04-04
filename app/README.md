# 🚀 Finance Dashboard Backend API

## 📌 Overview
This project is a backend system for a finance dashboard that manages financial records with role-based access control and analytics.

It allows different users (Admin, Analyst, Viewer) to interact with financial data securely and efficiently.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite (can be upgraded to PostgreSQL)
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Token)
- **Validation:** Pydantic

---

## 👥 User Roles

| Role     | Permissions |
|----------|-----------|
| Viewer   | View records & dashboard |
| Analyst  | View records + analytics |
| Admin    | Full access (CRUD + user management) |

---

## 🔐 Authentication

- JWT-based authentication
- Secure login with access tokens
- Token required for protected APIs

---

## 📦 Features

### 👤 User Management
- Register user
- Login with JWT
- Role-based access control

### 💰 Financial Records
- Create, Read, Update, Delete records
- Fields:
  - Amount
  - Type (income/expense)
  - Category
  - Date
  - Description
- Filtering:
  - By type
  - By category
  - By date range

### 📊 Dashboard Analytics
- Total income
- Total expenses
- Net balance
- Category-wise aggregation
- Monthly trends
- Recent transactions

### ⚡ Additional Features
- Pagination support
- Input validation
- Error handling
- Clean architecture

---

## 📡 API Endpoints

### 🔐 Auth
- `POST /auth/register`
- `POST /auth/login`

### 👥 Users
- `GET /users/` (Admin only)

### 💰 Records
- `POST /records/`
- `GET /records/`
- `GET /records/{id}`
- `PUT /records/{id}`
- `DELETE /records/{id}`

### 📊 Dashboard
- `GET /dashboard/summary`
- `GET /dashboard/category-wise`
- `GET /dashboard/recent`
- `GET /dashboard/monthly-trends`

---

## 🧪 Testing

Tested using:
- Swagger UI → `/docs`
- Postman

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/YOUR_USERNAME/finance-dashboard-backend.git
cd finance-dashboard-backend

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload