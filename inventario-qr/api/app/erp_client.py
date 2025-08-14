import requests
import os
import logging
from typing import List

from . import schemas

ERP_API_URL = os.getenv("ERP_API_URL")
ERP_API_TOKEN = os.getenv("ERP_API_TOKEN")

logger = logging.getLogger(__name__)

headers = {
    "Authorization": f"Bearer {ERP_API_TOKEN}",
    "Content-Type": "application/json"
}

def create_movimiento_salida(nota: schemas.Nota, items: List[schemas.NotaItem]) -> str:
    """Stub: Simula la creación de un movimiento de salida en el ERP."""
    payload = {
        "nota_id": str(nota.id),
        "almacen": nota.almacen,
        "solicitante": nota.creado_por,
        "items": [item.model_dump() for item in items]
    }
    logger.info(f"[ERP STUB] Creating movement with payload: {payload}")
    # In a real implementation:
    # response = requests.post(f"{ERP_API_URL}/movimientos/salida", json=payload, headers=headers)
    # response.raise_for_status()
    # return response.json()["mov_numero"]
    return f"MOV-SAL-{nota.id.hex[:6].upper()}"

def create_sc_intercompany(nota: schemas.Nota, item: schemas.NotaItem) -> str:
    """Stub: Simula la creación de una Solicitud de Compra intercompany."""
    payload = {
        "nota_id": str(nota.id),
        "empresa_compradora": nota.empresa_solicitante,
        "empresa_vendedora": item.empresa_origen,
        "item": item.model_dump()
    }
    logger.info(f"[ERP STUB] Creating intercompany SC with payload: {payload}")
    # In a real implementation:
    # response = requests.post(f"{ERP_API_URL}/sc/intercompany", json=payload, headers=headers)
    # response.raise_for_status()
    # return response.json()["sc_numero"]
    return f"SC-INT-{nota.id.hex[:4].upper()}-{item.linea}"
