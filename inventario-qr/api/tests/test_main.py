import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure the application package is importable
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent))

# Configure in-memory SQLite for tests before importing the app
os.environ['DB_URL'] = 'sqlite:///:memory:'

import app.database as database  # noqa: E402
database.Base.metadata.create_all = lambda bind=None: None

from app.main import app  # noqa: E402

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de Inventario QR"}
