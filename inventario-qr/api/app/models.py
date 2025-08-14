from sqlalchemy import (Column, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .database import Base

class EncabezadoNota(Base):
    __tablename__ = "encabezados_notas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    estado = Column(String, nullable=False, default="BORRADOR")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    empresa_solicitante = Column(String, nullable=False)
    filial = Column(String, nullable=False)
    almacen = Column(String, nullable=False)
    centro_costo = Column(String, nullable=True)
    creado_por = Column(String, nullable=False)
    firmas_json = Column(JSONB, nullable=True)
    hash = Column(String, nullable=True)

    items = relationship("DetalleNotaItem", back_populates="nota", cascade="all, delete-orphan")

class DetalleNotaItem(Base):
    __tablename__ = "detalles_notas_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nota_id = Column(UUID(as_uuid=True), ForeignKey("encabezados_notas.id"), nullable=False)
    linea = Column(Integer, nullable=False)
    producto = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=False)
    um = Column(String, nullable=False)
    factor_empaque = Column(Integer, nullable=False)
    cantidad_entregada = Column(Integer, nullable=False)
    cantidad_devuelta = Column(Integer, nullable=False, server_default="0")
    requiere_lote = Column(Boolean, nullable=False)
    lote = Column(String, nullable=True)
    serie = Column(String, nullable=True)
    empresa_origen = Column(String, nullable=True)
    intercompany = Column(Boolean, nullable=False, server_default="false")
    estado_regularizacion = Column(String, nullable=True)
    sc_numero = Column(String, nullable=True)
    motivo = Column(String, nullable=True)
    observacion = Column(String, nullable=True)

    nota = relationship("EncabezadoNota", back_populates="items")

    __table_args__ = (UniqueConstraint('nota_id', 'linea', name='_nota_linea_uc'),)
