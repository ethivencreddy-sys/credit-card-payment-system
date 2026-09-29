# Credit Card Payment System

A backend application for managing users, saved credit/debit cards, and credit card payments.

## Technologies Used

- Python 3.10
- Django
- Django REST Framework
- FastAPI
- MySQL 8.0
- SQLAlchemy/Django ORM
- JWT Authentication
- Docker & Docker Compose
- Postman
- Swagger/OpenAPI
- Coverage.py

## Project Features

### 1. User Authentication
- User registration
- JWT login
- JWT token refresh
- Logout with refresh-token blacklisting
- Password hashing using Django authentication

### 2. Card Management
- Add credit/debit cards
- View saved cards
- Delete saved cards
- Full card numbers are not stored
- Card numbers are masked
- Only the last four digits are stored
- CVV is not stored

### 3. Payment Processing
- FastAPI payment service
- Payment amount validation
- Card and user validation
- Initial transaction status: `PENDING`
- Simulated payment result: `SUCCESS` or `FAILED`
- Unique transaction reference

### 4. Transaction Management
- View transaction history
- Filter by status
- Filter by minimum/maximum amount
- Filter by start/end date
- Daily payment summary
- Admin CSV export

### 5. Admin
- Manage users
- Manage saved cards
- Manage transactions
- View transaction status
- Export transactions as CSV
- Daily transaction summary

## API Endpoints

### Django API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/token/refresh/` | Refresh JWT |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/cards/` | List cards |
| POST | `/api/cards/` | Add card |
| DELETE | `/api/cards/{id}/` | Delete card |
| GET | `/api/transactions/` | List transactions |
| GET | `/api/transactions/daily-summary/` | Daily summary |
| GET | `/api/docs/` | Django API documentation |

### FastAPI

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/payments/` | Process payment |
| GET | `/docs` | FastAPI Swagger documentation |

## Database

Database name:

`credit_card_payment_system`

Main tables:

- Users
- Cards
- Transactions

The database backup is included as:

`credit_card_payment_system.sql`

## Docker

The project uses Docker Compose with three services:

- MySQL
- Django
- FastAPI

Start the services:

```bash
docker compose up -d