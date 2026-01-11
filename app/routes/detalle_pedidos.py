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


@router.post("/detalle_pedidos/", response_model=schemas.DetallePedido, status_code=status.HTTP_201_CREATED)
async def create_detalle_pedido(
    detalle_pedido: schemas.DetallePedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if idPedido exists
        pedido_exists = await db.pedido.find_unique(where={'idPedido': detalle_pedido.idPedido})
        if not pedido_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pedido not found")

        # Check if idProducto exists and get its price
        producto = await db.producto.find_unique(where={'idProducto': detalle_pedido.idProducto})
        if not producto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Producto not found")
        
        # Calculate Total
        precio_unitario = detalle_pedido.Precio if detalle_pedido.Precio > 0 else producto.Precio
        total_calculated = precio_unitario * detalle_pedido.Cantidad

        created_detalle_pedido = await db.detallepedido.create(data={
            "idPedido": detalle_pedido.idPedido,
            "idProducto": detalle_pedido.idProducto,
            "Precio": precio_unitario,
            "Cantidad": detalle_pedido.Cantidad,
            "Total": total_calculated,
            "createdBy": current_user.username,
            "updatedBy": current_user.username
        })
        return created_detalle_pedido
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/detalle_pedidos/", response_model=list[schemas.DetallePedido])
async def read_detalle_pedidos(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    detalle_pedidos = await db.detallepedido.find_many(include={'pedido': True, 'producto': True})
    return detalle_pedidos


@router.get("/detalle_pedidos/{detalle_pedido_id}", response_model=schemas.DetallePedido)
async def read_detalle_pedido(
    detalle_pedido_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    detalle_pedido = await db.detallepedido.find_unique(where={'id': detalle_pedido_id}, include={'pedido': True, 'producto': True})
    if detalle_pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DetallePedido not found")
    return detalle_pedido


@router.put("/detalle_pedidos/{detalle_pedido_id}", response_model=schemas.DetallePedido)
async def update_detalle_pedido(
    detalle_pedido_id: str,
    detalle_pedido: schemas.DetallePedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Check if idPedido exists
        pedido_exists = await db.pedido.find_unique(where={'idPedido': detalle_pedido.idPedido})
        if not pedido_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pedido not found")

        # Check if idProducto exists and get its price
        producto = await db.producto.find_unique(where={'idProducto': detalle_pedido.idProducto})
        if not producto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Producto not found")
        
        # Calculate Total
        precio_unitario = detalle_pedido.Precio if detalle_pedido.Precio > 0 else producto.Precio
        total_calculated = precio_unitario * detalle_pedido.Cantidad

        updated_detalle_pedido = await db.detallepedido.update(
            where={'id': detalle_pedido_id},
            data={
                "idPedido": detalle_pedido.idPedido,
                "idProducto": detalle_pedido.idProducto,
                "Precio": precio_unitario,
                "Cantidad": detalle_pedido.Cantidad,
                "Total": total_calculated,
                "updatedBy": current_user.username
            }
        )
        return updated_detalle_pedido
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DetallePedido not found or error during update")


@router.delete("/detalle_pedidos/{detalle_pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detalle_pedido(
    detalle_pedido_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        await db.detallepedido.delete(where={'id': detalle_pedido_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DetallePedido not found or error during delete")
