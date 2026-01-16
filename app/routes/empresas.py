from fastapi import APIRouter, HTTPException, status, Depends
from prisma import Prisma
from app import schemas
from app.routes.auth import get_current_active_user
from typing import List

router = APIRouter()

# Dependencia para obtener la instancia de Prisma
async def get_prisma_client():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

@router.post("/empresas/", response_model=schemas.Empresa, status_code=status.HTTP_201_CREATED)
async def create_empresa(
    empresa: schemas.EmpresaBase,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    try:
        # Se insertan los datos según tu modelo Prisma 
        created_empresa = await db.empresa.create(data={
            "RazonSocial": empresa.RazonSocial,
            "idPedido": empresa.idPedido,
            "idRecibo": empresa.idRecibo
        })
        return created_empresa
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/empresas/", response_model=List[schemas.Empresa])
async def read_empresas(
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    return await db.empresa.find_many()

@router.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
async def read_empresa(
    empresa_id: int,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    empresa = await db.empresa.find_unique(where={'idEmpresa': empresa_id})
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    return empresa

@router.put("/empresas/{empresa_id}", response_model=schemas.Empresa)
async def update_empresa(
    empresa_id: int,
    empresa: schemas.EmpresaBase,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    try:
        updated = await db.empresa.update(
            where={'idEmpresa': empresa_id},
            data={
                'RazonSocial': empresa.RazonSocial,
                'idPedido': empresa.idPedido,
                'idRecibo': empresa.idRecibo
            }
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al actualizar la empresa")

@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_empresa(
    empresa_id: int,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    try:
        await db.empresa.delete(where={'idEmpresa': empresa_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada o error al eliminar")