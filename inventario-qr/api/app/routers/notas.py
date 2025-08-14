import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import schemas, models, crud, security, pdf_generator
from app.database import get_db
from common.py.types import generate_hmac_hash

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Nota, status_code=status.HTTP_201_CREATED)
def create_nota(
    nota: schemas.NotaEncabezadoCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    """Crea una nueva nota de inventario en estado BORRADOR."""
    return crud.create_nota(db=db, nota_encabezado=nota, username=current_user.username)

@router.get("/{nota_id}", response_model=schemas.Nota)
def read_nota(nota_id: UUID, db: Session = Depends(get_db)):
    """Obtiene los detalles de una nota de inventario existente."""
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if db_nota is None:
        raise HTTPException(status_code=404, detail="Nota not found")
    return db_nota

@router.post("/{nota_id}/items", response_model=schemas.Nota)
def add_or_update_item(
    nota_id: UUID,
    item: schemas.NotaItemCreate,
    db: Session = Depends(get_db)
):
    """Agrega o actualiza un item en una nota. La lógica de si es nuevo o no está en el CRUD."""
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if not db_nota or db_nota.estado == "FINALIZADA":
        raise HTTPException(status_code=400, detail="Nota no válida o ya finalizada")
    
    return crud.add_or_update_item_in_nota(db=db, nota_id=nota_id, item=item)

@router.post("/{nota_id}/firmas", response_model=schemas.Nota)
def save_firmas(
    nota_id: UUID,
    firmas: schemas.FirmaSchema,
    db: Session = Depends(get_db)
):
    """Guarda las firmas (solicitante y entrega) en la nota."""
    return crud.save_firmas_in_nota(db, nota_id=nota_id, firmas=firmas)

@router.post("/{nota_id}/finalizar", response_model=schemas.Nota)
def finalizar_nota(
    nota_id: UUID,
    db: Session = Depends(get_db)
):
    """Finaliza la nota, realiza validaciones y genera movimientos en el ERP."""
    final_nota = crud.finalize_nota(db, nota_id=nota_id)
    if not final_nota:
        raise HTTPException(status_code=400, detail="Error al finalizar la nota. Verifique los datos.")
    
    # Generar hash y PDF post-finalización
    final_nota.hash = generate_hmac_hash(str(final_nota.id))
    db.commit()
    db.refresh(final_nota)

    pdf_generator.generate_nota_pdf(final_nota)

    return final_nota

@router.get("/{nota_id}/pdf", response_class=Response)
def get_nota_pdf(nota_id: UUID, db: Session = Depends(get_db)):
    """Descarga el PDF del comprobante de la nota."""
    db_nota = crud.get_nota(db, nota_id=nota_id)
    if not db_nota or db_nota.estado != "FINALIZADA":
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="PDF no disponible para esta nota.")

    pdf_path = pdf_generator.get_pdf_path(nota_id)
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        return Response(content=pdf_bytes, media_type="application/pdf")
    except FileNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Archivo PDF no encontrado.")
