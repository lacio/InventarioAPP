from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import UUID
import hmac
import hashlib
import os

# Shared Enums
EstadoNota = Literal["BORRADOR", "FINALIZADA"]
EstadoRegularizacion = Literal["PEND_REG", "REG_OK"]

class Firma(BaseModel):
    solicitante: str  # Base64 PNG
    entrega: str      # Base64 PNG

class NotaItemBase(BaseModel):
    producto: str
    descripcion: str
    um: str
    factor_empaque: int
    cantidad_entregada: int
    requiere_lote: bool
    lote: Optional[str] = None
    serie: Optional[str] = None
    intercompany: bool = False
    empresa_origen: Optional[str] = None

class NotaItem(NotaItemBase):
    linea: int
    cantidad_devuelta: int = 0
    estado_regularizacion: Optional[EstadoRegularizacion] = None
    sc_numero: Optional[str] = None
    motivo: Optional[str] = None
    observacion: Optional[str] = None

class NotaBase(BaseModel):
    empresa_solicitante: str
    filial: str
    almacen: str
    centro_costo: Optional[str] = None

class Nota(NotaBase):
    id: UUID
    estado: EstadoNota
    items: List[NotaItem] = []
    firmas: Optional[Firma] = None
    hash: Optional[str] = None

# Utility
def generate_hmac_hash(data: str) -> str:
    secret = os.getenv("HMAC_SECRET", "").encode('utf-8')
    message = data.encode('utf-8')
    return hmac.new(secret, message, hashlib.sha256).hexdigest()
