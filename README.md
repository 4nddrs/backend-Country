# 🚀 Backend - FastAPI API

This is the backend service for the project, built with **FastAPI**.  
It provides a RESTful API to handle business logic, database operations, and integration with external services.

## 📖 Overview
This backend is designed to be modular and scalable, allowing easy addition of new features and services...
---

## 📂 Project Structure
```bash
backend/
├── app/
│   ├── main.py # Entry point of the application
│   ├── crud/ # Handles database operations (Create, Read, Update, Delete)
│   ├── routers/ # API route definitions for different modules
│   ├── schemas/ # Pydantic models for data validation and serialization
│   ├── services/ # Contains business logic and service layer
│   ├── utils/ # Helper functions and utilities
│   ├── config.py # Configuration and environment variables
│   └── supabase_client.py # Integration with Supabase (if used)
├── requirements.txt # Python dependencies
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10 or newer
- pip
- Virtual environment (recommended)
- (Optional) PostgreSQL or other database if configured

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-backend-repo.git
cd your-backend-repo
```
### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

▶️ Running the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at: http://127.0.0.1:8000

Interactive API docs:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

---

## 🛠 Development
- Follow PEP8 guidelines for Python code.
- Use `.env` file for secrets and configuration.
- Add new routes inside the `routers/` folder and import them in `main.py`.

---

## 📘 Examples of API Usage

### 1. Get All Employees
**Endpoint**: `GET /employees`
```bash
curl -X GET http://127.0.0.1:8000/employees
```
**Response**:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "position": "Manager"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "position": "Developer"
  }
]
```

### 2. Add a New Horse
**Endpoint**: `POST /horses`
```bash
curl -X POST http://127.0.0.1:8000/horses \
-H "Content-Type: application/json" \
-d '{"name": "Thunder", "age": 5, "owner_id": 1}'
```
**Response**:
```json
{
  "id": 1,
  "name": "Thunder",
  "age": 5,
  "owner_id": 1
}
```

### 3. Update Employee Position
**Endpoint**: `PUT /employees/{id}`
```bash
curl -X PUT http://127.0.0.1:8000/employees/1 \
-H "Content-Type: application/json" \
-d '{"position": "Senior Manager"}'
```
**Response**:
```json
{
  "id": 1,
  "name": "John Doe",
  "position": "Senior Manager"
}
```

### 4. Delete a Horse
**Endpoint**: `DELETE /horses/{id}`
```bash
curl -X DELETE http://127.0.0.1:8000/horses/1
```
**Response**:
```json
{
  "detail": "Horse deleted successfully."
}
```