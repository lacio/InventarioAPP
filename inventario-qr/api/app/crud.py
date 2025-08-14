from sqlalchemy.orm import Session, joinedload
from uuid import UUID
import logging

from . import models, schemas, erp_client

logger = logging.getLogger(__name__)

def get_nota(db: Session, nota_id: UUID):
    return db.query(models.EncabezadoNota).options(joinedload(models.EncabezadoNota.items)).filter(models.EncabezadoNota.id == nota_id).first()

def create_nota(db: Session, nota_encabezado: schemas.NotaEncabezadoCreate, username: str):
    db_nota = models.EncabezadoNota(**nota_encabezado.model_dump(), creado_por=username)
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

def add_or_update_item_in_nota(db: Session, nota_id: UUID, item: schemas.NotaItemCreate):
    nota = get_nota(db, nota_id)
    if not nota:
        return None

    # Check if item already exists
    existing_item = next((i for i in nota.items if i.producto == item.producto), None)

    if existing_item:
        # Update existing item
        existing_item.cantidad_entregada = item.cantidad_entregada
        existing_item.lote = item.lote
        existing_item.serie = item.serie
        existing_item.intercompany = item.intercompany
        existing_item.empresa_origen = item.empresa_origen
    else:
        # Add new item
        linea = len(nota.items) + 1
        db_item = models.DetalleNotaItem(
            **item.model_dump(), 
            nota_id=nota_id, 
            linea=linea
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(nota)
    return nota

def save_firmas_in_nota(db: Session, nota_id: UUID, firmas: schemas.FirmaSchema):
    nota = get_nota(db, nota_id)
    if not nota:
        return None
    nota.firmas_json = firmas.model_dump()
    db.commit()
    db.refresh(nota)
    return nota

def finalize_nota(db: Session, nota_id: UUID):
    nota = get_nota(db, nota_id)
    if not nota or nota.estado == 'FINALIZADA':
        return None

    items_normales = [item for item in nota.items if not item.intercompany]
    items_intercompany = [item for item in nota.items if item.intercompany]

    # Process normal items
    if items_normales:
        try:
            mov_numero = erp_client.create_movimiento_salida(nota, items_normales)
            logger.info(f"Movimiento de salida {mov_numero} creado para nota {nota.id}")
        except Exception as e:
            logger.error(f"Error creando movimiento de salida para nota {nota.id}: {e}")
            # In a real scenario, you might want to stop the process here
            return None

    # Process intercompany items
    for item in items_intercompany:
        try:
            sc_numero = erp_client.create_sc_intercompany(nota, item)
            item.sc_numero = sc_numero
            item.estado_regularizacion = "PEND_REG"
            logger.info(f"SC Intercompany {sc_numero} creada para item {item.producto} en nota {nota.id}")
        except Exception as e:
            logger.error(f"Error creando SC intercompany para item {item.producto} en nota {nota.id}: {e}")
            return None

    nota.estado = "FINALIZADA"
    db.commit()
    db.refresh(nota)
    return nota
