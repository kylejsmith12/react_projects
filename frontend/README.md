# People Manager Desktop App - Setup Guide

Complete guide to set up and run the full-stack desktop application.

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.9 or higher)
- **PostgreSQL** (v13 or higher)

## Database Setup

### 1. Install PostgreSQL
If you don't have PostgreSQL installed:
- **Windows**: Download from https://www.postgresql.org/download/windows/
- **macOS**: `brew install postgresql@15`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### 2. Start PostgreSQL Service
- **Windows**: PostgreSQL service should start automatically
- **macOS**: `brew services start postgresql@15`
- **Linux**: `sudo systemctl start postgresql`

### 3. Create Database
```bash
# Access PostgreSQL as postgres user
psql -U postgres

# Create the database
CREATE DATABASE people_db;

# Exit psql
\q
```

**Note**: The backend will automatically create the tables when it starts.

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
mkdir backend
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Save the `requirements.txt` file in the backend directory, then:
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
Save the `main.py` file in the backend directory, then:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

You can test it by visiting `http://localhost:8000/docs` for the interactive API documentation.

## Frontend Setup (Vite + React + Electron)

### 1. Create Vite Project
```bash
# In your project root (outside backend folder)
npm create vite@latest frontend -- --template react-ts
cd frontend
```

### 2. Install Dependencies
Replace the `package.json` with the provided one, then:
```bash
npm install
```

### 3. Set Up Project Structure
Create the following directory structure:
```
frontend/
├── electron/
│   └── main.js
├── src/
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── interfaces.ts
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

Copy all the provided files to their respective locations.

### 4. Run in Development Mode

**Option A: Run web version only**
```bash
npm run dev
```
Visit `http://localhost:5173`

**Option B: Run Electron app**
In one terminal:
```bash
npm run dev
```

In another terminal:
```bash
npm run electron
```

Or use the combined command:
```bash
npm run electron:dev
```

## Testing the Application

1. Make sure PostgreSQL is running
2. Start the backend: `python main.py` (from backend directory)
3. Start the frontend: `npm run electron:dev` (from frontend directory)
4. The Electron desktop app should open automatically

## Building for Production

### Build Frontend
```bash
npm run build
```

### Build Electron App
```bash
npm run electron:build
```

The packaged app will be in the `release` folder.

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `pg_isready`
- Check if database exists: `psql -U postgres -l`
- Ensure no password is set for postgres user: `psql -U postgres` (should connect without password prompt)

### Backend Issues
- Make sure you're in the virtual environment
- Check if port 8000 is available
- View logs in the terminal where you ran `python main.py`

### Frontend Issues
- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
- Check if port 5173 is available
- Make sure backend is running before starting frontend

### CORS Issues
The backend is configured to allow all origins. If you still have CORS issues, make sure:
- Backend is running on port 8000
- Frontend is making requests to `http://localhost:8000`

## API Endpoints

- `GET /people` - Get all people
- `GET /people/{id}` - Get person by ID
- `POST /people` - Create new person
- `PUT /people/{id}` - Update person
- `DELETE /people/{id}` - Delete person

## File Structure Overview

```
project/
├── backend/
│   ├── venv/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── electron/
    │   └── main.js
    ├── src/
    │   ├── services/
    │   │   └── api.ts
    │   ├── types/
    │   │   └── interfaces.ts
    │   ├── App.tsx
    │   └── main.tsx
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── vite.config.ts
```

## Next Steps

- Add authentication
- Implement data validation
- Add loading states and better error handling
- Add pagination for large datasets
- Implement search and filtering
- Add unit tests