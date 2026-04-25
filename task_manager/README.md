# Task Manager API

This guide explains how to build a robust Task Management system from scratch using **FastAPI**, **SQLAlchemy (Async)**, and **PostgreSQL**.

---

## 🛠 1. Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10+**
- **PostgreSQL** (Create a database named `taskdb`)

---

## 2. Step-by-Step Development Process

### Step 1: Initialize Project & Virtual Environment

Open your terminal/command prompt and run:

```bash
mkdir task_manager
cd task_manager
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy alembic pydantic-settings python-jose[cryptography] passlib[bcrypt] asyncpg psycopg2
```

### Step 3: Define Project Structure

Create the following folder hierarchy:

```text
task_manager/
├── core/          # Security, Cache, Config
├── db/            # Session, Base Models
├── models/        # SQLAlchemy Models
├── schemas/       # Pydantic Schemas
├── routes/        # API Endpoints
├── services/      # Business Logic
└── utils/         # Helpers
```

## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd task_manager
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install fastapi uvicorn sqlalchemy alembic pydantic-settings python-jose[cryptography] passlib[bcrypt] asyncpg psycopg2
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the `task_manager` directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost/taskdb
   JWT_SECRET=your_super_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ENV=development
   ```

## 🗄 Database Setup

1. Ensure PostgreSQL is running and the database `taskdb` exists.
2. Run migrations to create the tables:
   ```bash
   alembic upgrade head
   ```

## 🏃 Running the Application

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

- **Interactive Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`

## 🔒 Security Implementation

The project uses `OAuth2PasswordBearer` for securing routes.

- **Hashing**: Passwords are hashed using `bcrypt` via Passlib.
- **JWT**: Tokens are signed with a `SECRET_KEY` and include an expiration time.
- **Protected Routes**: Use the `get_current_user` dependency to authorize requests.

## 📝 Logging & Utilities

- **Logger**: Task creations are logged to `task_log.txt` using the utility in `utils/logger.py`.
- **Cache**: `core/cache.py` provides a `set_cache` and `get_cache` functionality with Time-To-Live (TTL) support to reduce database load.

## 📜 License

This project is licensed under the MIT License.
