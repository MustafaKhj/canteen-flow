# Canteen-Flow: Campus Food Order System

Canteen-Flow is a professional campus food ordering and management system built for an Advanced Database Management Systems lab project. It follows the attached project report requirements but uses MongoDB only for the complete database. No MySQL is used anywhere in this version.

## What This Project Does

The system provides three role-based interfaces:

1. Student Interface
   - Login as student
   - Browse daily menu
   - Add items to cart
   - Place order
   - View personal order history

2. Staff Interface
   - View incoming orders
   - Update order status
   - Move order from pending to in preparation, ready, delivered, or cancelled

3. Admin Interface
   - View dashboard metrics
   - See revenue and order counts
   - See low-stock inventory
   - View feedback summary
   - Generate demand forecast from historical orders

## Database Requirement

The original report discusses MySQL plus MongoDB. This delivered version intentionally removes MySQL completely because the finalized instruction is to use MongoDB for the entire database.

MongoDB collections used:
- users
- menu_items
- orders
- order_items
- payments
- transactions
- inventory
- stock_logs
- feedback
- forecasts

## Academic Requirements Covered

- Database Schema: docs/DATABASE_SCHEMA.md
- ER Diagram: docs/ER_DIAGRAM_MONGODB.md
- Normalized Tables: implemented as normalized MongoDB collections with references
- CRUD Functionalities: menu, orders, inventory, feedback, users/auth
- Frontend Interface: frontend/index.html, frontend/assets/styles.css, frontend/assets/app.js
- MongoDB Integration: backend/db.py with PyMongo
- Backend API: Flask REST API with routes in backend/routes
- Demand Forecasting: backend/services/forecast_service.py
- Documentation: README and docs folder

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python Flask
- Flask-CORS
- PyMongo
- JWT authentication
- Werkzeug password hashing

Database:
- MongoDB only

## Folder Structure

```text
canteen-flow-mongodb/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── routes/
│   ├── services/
│   └── utils/
├── database/
│   └── seed.py
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   └── ER_DIAGRAM_MONGODB.md
├── frontend/
│   ├── index.html
│   └── assets/
├── requirements.txt
├── .env.example
├── run.py
└── README.md
```

## How To Run Locally

### 1. Install MongoDB
Install MongoDB Community Server and make sure MongoDB service is running.

Default local URI:
```text
mongodb://localhost:27017
```

### 2. Open Project in VS Code
Open the folder `canteen-flow-mongodb` in VS Code.

### 3. Create Virtual Environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Setup Environment File
Copy `.env.example` and rename it to `.env`.

### 6. Seed Demo Data
```bash
python database/seed.py
```

Demo accounts:
```text
Student: student@canteenflow.edu / student123
Staff: staff@canteenflow.edu / staff123
Admin: admin@canteenflow.edu / admin123
```

### 7. Run the Project
```bash
python run.py
```

Open browser:
```text
http://localhost:5000
```

## Current Project Status

Completed in this version:
- MongoDB-only database design
- Flask backend structure
- JWT authentication
- Role-based access
- Menu CRUD backend
- Order placement
- Staff order status update
- Admin dashboard
- Inventory APIs
- Feedback APIs
- Demand forecast endpoint
- Professional responsive frontend
- Seed data
- Documentation files

Not included yet:
- External payment gateway
- Mobile app
- Real-time push notifications
- Production-level security hardening
- Cloud deployment configuration

## Developer Continuation Prompt

Use this prompt in another AI chat if you continue development:

I am building Canteen-Flow, a campus food order system for an Advanced Database Management Systems lab project. The attached report originally mentions MySQL + MongoDB, but the finalized requirement is MongoDB only for the entire database. Do not use MySQL anywhere. The project already has a Flask backend, PyMongo integration, JWT authentication, MongoDB collections for users, menu_items, orders, order_items, payments, transactions, inventory, stock_logs, feedback, and forecasts, plus a professional HTML/CSS/JS frontend. Keep the design minimal, aesthetic, and Tech Venture presentation-ready. Continue from the existing folder structure and preserve compatibility with `python run.py`, `python database/seed.py`, and `http://localhost:5000`.
