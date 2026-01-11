from fastapi import APIRouter, HTTPException, status, Depends
from prisma import Prisma
from app import schemas
from app.routes.auth import get_current_active_user

router = APIRouter()

# Dependency to get a Prisma client instance
async def get_prisma_client():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@router.post("/pedidos/", response_model=schemas.Pedido, status_code=status.HTTP_201_CREATED)
async def create_pedido(
    pedido: schemas.PedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idAsesor exists
        asesor_exists = await db.asesor.find_unique(where={'idAsesor': pedido.idAsesor})
        if not asesor_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asesor not found")

        # Check if the idCliente exists
        cliente_exists = await db.cliente.find_unique(where={'idCliente': pedido.idCliente})
        if not cliente_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente not found")

        created_pedido = await db.pedido.create(data={
            "fechaPedido": pedido.fechaPedido,
            "totalPedido": pedido.totalPedido,
            "Status": pedido.Status,
            "asesor": {
                "connect": {
                    "idAsesor": pedido.idAsesor
                }
            },
            "cliente": {  # Add cliente connection
                "connect": {
                    "idCliente": pedido.idCliente
                }
            },
            "createdBy": current_user.username,
            "updatedBy": current_user.username
        })
        return created_pedido
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/pedidos/", response_model=list[schemas.Pedido])
async def read_pedidos(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    pedidos = await db.pedido.find_many(include={'asesor': True, 'cliente': True}) # Include cliente
    return pedidos


@router.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def read_pedido(
    pedido_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    pedido = await db.pedido.find_unique(where={'idPedido': pedido_id}, include={'asesor': True, 'cliente': True}) # Include cliente
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    return pedido


@router.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def update_pedido(
    pedido_id: str,
    pedido: schemas.PedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if the idAsesor exists if it's being updated
        if pedido.idAsesor:
            asesor_exists = await db.asesor.find_unique(where={'idAsesor': pedido.idAsesor})
            if not asesor_exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asesor not found")

        # Check if the idCliente exists if it's being updated
        if pedido.idCliente:
            cliente_exists = await db.cliente.find_unique(where={'idCliente': pedido.idCliente})
            if not cliente_exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente not found")

        updated_pedido = await db.pedido.update(
            where={'idPedido': pedido_id},
            data={
                "fechaPedido": pedido.fechaPedido,
                "totalPedido": pedido.totalPedido,
                "Status": pedido.Status,
                "asesor": {
                    "connect": {
                        "idAsesor": pedido.idAsesor
                    }
                },
                "cliente": {  # Add cliente connection
                    "connect": {
                        "idCliente": pedido.idCliente
                    }
                },
                "updatedBy": current_user.username
            }
        )
        return updated_pedido
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found or error during update")


@router.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido(
    pedido_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        await db.pedido.delete(where={'idPedido': pedido_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found or error during delete")
