from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routers import auth, notas, catalogo
from app.database import Base, engine

load_dotenv()

# This is for Alembic to create the tables
# In a real app, you might handle this with a migration command
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventario QR API",
    description="API para gestionar salidas y devoluciones de inventario con QR.",
    version="1.0.0"
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(catalogo.router, prefix="/catalogo", tags=["Catalogo"])
app.include_router(notas.router, prefix="/notas", tags=["Notas de Inventario"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de Inventario QR"}
