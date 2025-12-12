Organization Management Backend (Multi-Tenant)

A FastAPI backend service that manages organizations with full lifecycle support — creation, authentication, update, and deletion — using JWT-based authentication and a multi-tenant MongoDB design.

The project also includes a minimal dark-themed demo UI to visually demonstrate that the APIs work end-to-end in a real browser environment.

✨ Key Features

🏢 Create organizations with an admin account

🔐 Admin authentication using JWT (OAuth2 flow)

🧩 Multi-tenant MongoDB architecture (one collection per organization)

✏️ Update organization name and admin credentials

🗑️ Delete organizations and associated collections

🌐 CORS-enabled for browser clients

🧪 Fully tested via Swagger, curl/PowerShell, and demo UI

🛠️ Tech Stack

Backend: FastAPI (Python)

Database: MongoDB (MongoDB Atlas)

Authentication: JWT (OAuth2PasswordBearer)

Password Hashing: bcrypt (via passlib)

Frontend (Demo Only): HTML, CSS, Vanilla JavaScript

📂 Project Structure
organization-management-backend/
│
├── app/
│   ├── main.py          # FastAPI app + CORS middleware
│   ├── routers.py       # API route definitions
│   ├── services.py      # Business logic
│   ├── auth.py          # JWT handling & password hashing
│   ├── database.py     # MongoDB connection & collections
│   ├── models.py       # Pydantic request/response models
│   └── config.py       # Environment variable configuration
│
├── demo-ui/
│   └── index.html       # Dark-themed demo UI
│
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Environment Configuration

The application uses environment variables for all sensitive configuration.
The .env file is intentionally excluded from version control.

Required Variables
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
MASTER_DB_NAME=master_db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60


In production, these values are configured directly on the deployment platform (e.g., Render).

▶️ Running the Backend Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start the server
uvicorn app.main:app --reload


Backend runs at:

http://127.0.0.1:8000

📑 API Documentation (Swagger)

FastAPI provides interactive API docs:

http://127.0.0.1:8000/docs


Swagger can be used to:

Create organizations

Login as admin

Test protected routes

🔐 Authentication Flow

An organization is created with an admin email & password

Admin logs in via /admin/login

A JWT access token is returned

Token must be sent as:

Authorization: Bearer <token>


Protected endpoints:

PUT /org/update

DELETE /org/delete

🧩 Multi-Tenant Architecture

A master database stores metadata about all organizations

Each organization gets its own MongoDB collection

Collection names are generated dynamically

On update:

Organization name and collection are renamed

On delete:

Organization metadata and collection are removed

This ensures clean isolation between tenants.

🌐 Demo UI (API Validation UI)

The project includes a minimal browser-based demo UI located at:

demo-ui/index.html

Purpose of the UI

The UI is not a product frontend

It exists purely to demonstrate API correctness

Shows live JSON responses from the backend

Features

Create Organization

Admin Login

Update Organization

Delete Organization

Displays real-time API responses

How to Use

Start the backend

Open demo-ui/index.html in a browser

Follow the flow:

Create → Login → Update → Delete

The UI communicates directly with the backend using fetch() and validates:

CORS configuration

Authentication flow

Protected endpoints

🧪 Testing & Verification

All endpoints were tested using:

Swagger UI

PowerShell / curl

Demo UI (browser-based)

Verified Endpoints
Method	Endpoint	Description
POST	/org/create	Create organization
POST	/admin/login	Admin login (JWT)
PUT	/org/update	Update org details
DELETE	/org/delete	Delete organization
🔒 Security Notes

Passwords are hashed using bcrypt

JWT tokens are validated on every protected request

Secrets are never committed to GitHub

Environment variables are used for all sensitive data

🏁 Summary

This project demonstrates:

Clean backend architecture

Secure authentication

Multi-tenant database design

Proper environment variable handling

End-to-end verification using a demo UI

The focus is intentionally on backend correctness and system design, with the UI serving as a lightweight validation layer.
