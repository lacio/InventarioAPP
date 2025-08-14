from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Mock data from ERP catalog
CATALOGO_ERP = {
    "PROD001": {"descripcion": "Tornillo Phillips", "um": "UN", "factor_empaque": 1, "requiere_lote": False, "requiere_serie": False, "stock": {"EMPRESA_A": 100, "EMPRESA_B": 50}},
    "PROD002": {"descripcion": "Caja de 100 Guantes de Nitrilo", "um": "CAJA", "factor_empaque": 100, "requiere_lote": True, "requiere_serie": False, "stock": {"EMPRESA_A": 20, "EMPRESA_B": 80}},
    "PROD003": {"descripcion": "Taladro Inalambrico", "um": "UN", "factor_empaque": 1, "requiere_lote": False, "requiere_serie": True, "stock": {"EMPRESA_A": 0, "EMPRESA_B": 15}},
}

@router.get("/{codigo}")
async def get_info_producto(codigo: str):
    """Valida un código de producto contra el catálogo y devuelve su información."""
    if codigo not in CATALOGO_ERP:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con código '{codigo}' no encontrado.")
    
    # In a real scenario, this would also check stock via erp_client
    return CATALOGO_ERP[codigo]
