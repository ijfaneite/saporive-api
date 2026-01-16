from fastapi import APIRouter, HTTPException, status, Depends
from prisma import Prisma
from app import schemas
from app.routes.auth import get_current_active_user # Import get_current_active_user

router = APIRouter()

# Dependency to get a Prisma client instance
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
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idEmpresa exists
        asesor_exists = await db.asesor.find_unique(where={'idEmpresa': empresa.idEmpresa})
        if not asesor_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empresa not found")

        created_empresa = await db.empresa.create(data={
            "RazonSocial": empresa.RazonSocial,
            "idPedido": empresa.idPedido,
            "idRecibo": empresa.idRecibo
        })
        return created_empresa
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/empresas/", response_model=list[schemas.Empresa])
async def read_empresas(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    empresas = await db.empresa.find_many(include={'asesor': True})
    return empresas


@router.get("/empresas/{empresa_id}", response_model=schemas.Empresa)
async def read_empresa(
    empresa_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    empresa = await db.empresa.find_unique(where={'idEmpresa': empresa_id}, include={'asesor': True})
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empresa not found")
    return empresa


@router.put("/empresas/{empresa_id}", response_model=schemas.Empresa)
async def update_empresa(
    empresa_id: str,
    empresa: schemas.Empresa,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idEmpresa exists if it's being updated
        if empresa.idEmpresa:
            asesor_exists = await db.asesor.find_unique(where={'idEmpresa': empresa.idEmpresa})
            if not asesor_exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empresa not found")

        updated_empresa = await db.empresa.update(
            where={'idempresa': empresa_id},
            data={
                "RazonSocial": empresa.RazonSocial,
                "idPedido": empresa.idPedido,
                "idRecibo": empresa.idRecibo,
            }
        )
        return updated_empresa
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empresa not found or error during update")


@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_empresa(
    empresa_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        await db.empresa.delete(where={'idEmpresa': empresa_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="empresa not found or error during delete")