# Ads Bot API

A FastAPI-based backend for managing classified ads via a chat interface (e.g., Telegram).  
Supports categories, file attachments, comments, and MongoDB as the data store.

---

## How to Launch the API

### 1. Clone or download the project
Unzip the archive or clone the repository.

### 2. Open terminal and navigate to the project folder:
```bash
cd api
```

### 3. Create a virtual environment (Python 3.11 required):
```bash
py -3.11 -m venv .venv
```

### 4. (Optional) Allow script execution (for PowerShell):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 5. Activate the virtual environment:
```powershell
.venv\Scripts\Activate.ps1
```

### 6. Install required dependencies:
```bash
pip install -r requirements.txt
```

### 7. Go back to root folder:
```bash
cd ..
```

### 8. Run the FastAPI server:
```bash
python -m uvicorn api.main:app --reload
```

---

## API Documentation

Once the server is running, visit:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
