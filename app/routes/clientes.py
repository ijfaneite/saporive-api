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


@router.post("/clientes/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente(
    cliente: schemas.ClienteCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idAsesor exists
        asesor_exists = await db.asesor.find_unique(where={'idAsesor': cliente.idAsesor})
        if not asesor_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asesor not found")

        created_cliente = await db.cliente.create(data={
            "Rif": cliente.Rif,
            "Cliente": cliente.Cliente,
            "Zona": cliente.Zona,
            "asesor": {
                "connect": {
                    "idAsesor": cliente.idAsesor
                }
            },
            "createdBy": current_user.username,
            "updatedBy": current_user.username
        })
        return created_cliente
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/clientes/", response_model=list[schemas.Cliente])
async def read_clientes(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    clientes = await db.cliente.find_many(include={'asesor': True})
    return clientes


@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def read_cliente(
    cliente_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    cliente = await db.cliente.find_unique(where={'idCliente': cliente_id}, include={'asesor': True})
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")
    return cliente


@router.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
async def update_cliente(
    cliente_id: str,
    cliente: schemas.ClienteCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idAsesor exists if it's being updated
        if cliente.idAsesor:
            asesor_exists = await db.asesor.find_unique(where={'idAsesor': cliente.idAsesor})
            if not asesor_exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asesor not found")

        updated_cliente = await db.cliente.update(
            where={'idCliente': cliente_id},
            data={
                "Rif": cliente.Rif,
                "Cliente": cliente.Cliente,
                "Zona": cliente.Zona,
                "asesor": {
                    "connect": {
                        "idAsesor": cliente.idAsesor
                    }
                },
                "updatedBy": current_user.username
            }
        )
        return updated_cliente
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found or error during update")


@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    cliente_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        await db.cliente.delete(where={'idCliente': cliente_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found or error during delete")