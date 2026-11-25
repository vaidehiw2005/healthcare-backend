# Healthcare Backend API

A RESTful backend built with Django, Django REST Framework (DRF), and PostgreSQL for managing users, patient records, doctor profiles, and patient-doctor assignments.

## Overview

I built this backend with a modular two-app architecture (`accounts` and `healthcare`) to keep authentication separate from core domain logic:
- Custom User & JWT Auth (`accounts`): Uses an email-based custom `User` model (`USERNAME_FIELD = 'email'`) paired with `djangorestframework-simplejwt` for token generation and validation.
- Data Isolation (`healthcare`): Patient records are tied to the user who created them (`created_by`), ensuring users can only view, update, or delete their own patients.
- Mapping Integrity: Patient–doctor assignments enforce a database-level `UniqueConstraint` alongside serializer validation to prevent duplicate mappings cleanly.

## Tech Stack

- Language & Framework: Python, Django 5.2, Django REST Framework
- Database: PostgreSQL (`psycopg2-binary`)
- Authentication: `djangorestframework-simplejwt`
- Environment Config: `python-dotenv`
- API Testing & Docs: Postman, `drf-spectacular` (Swagger UI)

## Project Structure

```text
healthcare-backend/
├── config/                  # Project settings and root URL routing
├── accounts/                # Custom User model, registration, and JWT login
├── healthcare/              # Patients, Doctors, Mappings models, views, serializers, and tests
├── postman/                 # Exported Postman collection (v2.1)
├── .env.example             # Sample environment configuration
├── manage.py
├── requirements.txt
└── README.md
```

## Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/vaidehiw2005/healthcare-backend.git](https://github.com/vaidehiw2005/healthcare-backend.git)
cd healthcare-backend
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL and environment variables
1. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE healthcare_db;
   ```
2. Copy `.env.example` to `.env` and fill in your local database credentials:
   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```

### 5. Apply migrations and run the server
```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/` (and interactive Swagger documentation at `http://127.0.0.1:8000/api/docs/`).

## Testing

### Postman
I tested all 15 endpoints using Postman and exported the collection to `postman/healthcare_api.postman_collection.json`.
1. Import `postman/healthcare_api.postman_collection.json` into Postman.
2. Call `POST /api/auth/register/` and `POST /api/auth/login/` to get an `access` token.
3. Paste the `access` token into the collection's `access_token` variable to run all protected requests.

### Automated Unit Tests
Run the Django test suite covering authentication, patient ownership isolation, doctor CRUD, and mapping constraints:
```bash
python manage.py test
```

## API Reference

### Authentication
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user (`name`, `email`, `password`) | No |
| `POST` | `/api/auth/login/` | Log in and receive `access` and `refresh` JWT tokens | No |
| `POST` | `/api/auth/token/refresh/` | Refresh an expired access token | No |

### Patients
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/patients/` | Add a new patient | Yes |
| `GET` | `/api/patients/` | List all patients created by the logged-in user | Yes |
| `GET` | `/api/patients/<id>/` | Retrieve a specific patient's details | Yes |
| `PUT` | `/api/patients/<id>/` | Update a patient's details | Yes |
| `DELETE` | `/api/patients/<id>/` | Delete a patient record | Yes |

### Doctors
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/doctors/` | Add a new doctor | Yes |
| `GET` | `/api/doctors/` | List all doctors | Yes |
| `GET` | `/api/doctors/<id>/` | Retrieve a specific doctor's details | Yes |
| `PUT` | `/api/doctors/<id>/` | Update a doctor's details | Yes |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor record | Yes |

### Patient–Doctor Mappings
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/mappings/` | Assign a doctor to a patient (`patient`, `doctor`) | Yes |
| `GET` | `/api/mappings/` | List all patient–doctor mappings | Yes |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors assigned to a specific patient | Yes |
| `DELETE` | `/api/mappings/<id>/` | Remove a doctor from a patient by mapping ID | Yes |