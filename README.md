# GestaltNotes

## Prerequisites

- Python 3.12+
- Poetry
- Node.js
- Firebase CLI (`npm install -g firebase-tools`)
- Java 11+ (required for Firebase emulators)

## Environment Setup

Needs a .env file for both frontend and backend folders

## Running Locally

Open three terminal windows:

**Terminal 1 — Backend API**

```bash
cd backend
poetry install
poetry run python src/main.py
```

**Terminal 2 — Firebase Emulators**

```bash
cd frontend
firebase emulators:start --project gestaltnotes
```

**Terminal 3 — Frontend**

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.  
The API docs (Swagger) will be available at `http://localhost:8000/docs`.  
The Firebase Emulator UI will be available at `http://localhost:4000`.

## Creating Test Users

With the backend and emulators running, use the Swagger UI at `http://localhost:8000/docs` to create test accounts.

**Create a student:**

```json
POST /users/
{
  "first_name": "Test",
  "last_name": "Student",
  "email": "student@test.com",
  "password": "password123",
  "role": "student"
}
```

**Create an educator:**

```json
POST /users/
{
  "first_name": "Test",
  "last_name": "Professor",
  "email": "professor@test.com",
  "password": "password123",
  "role": "educator"
}
```
