from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
from uuid import UUID

# Shared types from common module could be used here
# but defining explicitly for clarity in API layer.

# Base Schemas
class FirmaSchema(BaseModel):
    solicitante: str  # Base64 encoded PNG
    entrega: str      # Base64 encoded PNG

class NotaItemBase(BaseModel):
    producto: str
    descripcion: str
    um: str = Field(..., examples=["UN", "CAJA"])
    factor_empaque: int = Field(..., examples=[1, 12])
    cantidad_entregada: int
    requiere_lote: bool
    lote: Optional[str] = None
    serie: Optional[str] = None
    intercompany: bool = False
    empresa_origen: Optional[str] = None

class NotaEncabezadoBase(BaseModel):
    empresa_solicitante: str = Field(..., examples=["EMPRESA_A"])
    filial: str = Field(..., examples=["FILIAL_MADRID"])
    almacen: str = Field(..., examples=["ALMACEN_CENTRAL"])
    centro_costo: Optional[str] = None

# Schemas for Creation
class NotaItemCreate(NotaItemBase):
    pass

class NotaEncabezadoCreate(NotaEncabezadoBase):
    pass

# Schemas for Reading/Response
class NotaItem(NotaItemBase):
    linea: int
    cantidad_devuelta: int
    estado_regularizacion: Optional[Literal["PEND_REG", "REG_OK"]] = None
    sc_numero: Optional[str] = None

    class Config:
        from_attributes = True

class Nota(NotaEncabezadoBase):
    id: UUID
    estado: Literal["BORRADOR", "FINALIZADA"]
    creado_por: str
    items: List[NotaItem] = []
    firmas: Optional[FirmaSchema] = None
    hash: Optional[str] = None

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str
