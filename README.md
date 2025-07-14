# SautiDesk Model API

A FastAPI-based REST API for SautiDesk model predictions and data management.

## Project Structure

```
sautidesk-model/
├── app.py                 # Main FastAPI application entry point
├── routes/                # API route definitions
│   ├── __init__.py
│   ├── astra.py          # Astra-related endpoints
│   ├── create.py         # Create-related endpoints
│   ├── search.py         # Search-related endpoints
│   └── model.py          # Model-related endpoints
├── controllers/           # Business logic controllers
│   ├── __init__.py
│   ├── astra_controller.py
│   ├── create_controller.py
│   ├── search_controller.py
│   └── model_controller.py
└── requirements.txt       # Python dependencies
```

## API Endpoints

### Root Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check

### Astra Routes

- `GET /astra/` - Astra root endpoint
- `GET /astra/health` - Astra health check

### Create Routes

- `GET /create/` - Create root endpoint
- `GET /create/health` - Create health check

### Search Routes

- `GET /search/` - Search root endpoint
- `GET /search/health` - Search health check

### Model Routes

- `GET /model/` - Model root endpoint
- `GET /model/predict` - Model prediction endpoint
- `GET /model/health` - Model health check

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc
