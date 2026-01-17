from fastapi import APIRouter, HTTPException, status, Depends
from prisma import Prisma
from app import schemas
from app.routes.auth import get_current_active_user
from typing import List

router = APIRouter()

# Dependencia para conectar/desconectar Prisma en cada petición
async def get_prisma_client():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

# --- CREATE (Crear Pedido con Detalles) ---
@router.post("/pedidos/", response_model=schemas.Pedido, status_code=status.HTTP_201_CREATED)
async def create_pedido(
    pedido: schemas.PedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Validación de integridad: ¿Existe el asesor y el cliente?
        #async with db.batch_() as batch:
        #    batch.asesor.find_unique(where={'idAsesor': pedido.idAsesor})
        #    batch.cliente.find_unique(where={'idCliente': pedido.idCliente})

        # Creación atómica (Pedido + Detalles)
        created_pedido = await db.pedido.create(
            data={
                "idPedido": pedido.idPedido,
                "idEmpresa": pedido.idEmpresa,
                "fechaPedido": pedido.fechaPedido,
                "totalPedido": pedido.totalPedido,
                "Status": pedido.Status,
                "createdBy": current_user.username,
                "updatedBy": current_user.username,
                "asesor": {"connect": {"idAsesor": pedido.idAsesor}},
                "cliente": {"connect": {"idCliente": pedido.idCliente}},
                "detalles": {
                    "create": [
                        {
                            "idProducto": d.idProducto,
                            "Precio": d.Precio,
                            "Cantidad": d.Cantidad,
                            "Total": d.Precio * d.Cantidad,
                            "createdBy": current_user.username,
                            "updatedBy": current_user.username
                        } for d in pedido.detalles
                    ]
                }
            },
            include={"detalles": True, "asesor": True, "cliente": True}
        )
        return created_pedido
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear: {str(e)}")

# --- READ ALL (Listar con Detalles) ---
@router.get("/pedidos/", response_model=List[schemas.Pedido])
async def read_pedidos(
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    # 'include' es vital para traer las relaciones y que no lleguen vacías
    return await db.pedido.find_many(
        include={"detalles": True, "asesor": True, "cliente": True},
        order={"createdAt": "desc"}
    )

# --- READ ONE (Obtener por ID) ---
@router.get("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def read_pedido(
    pedido_id: str,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    pedido = await db.pedido.find_unique(
        where={'idPedido': pedido_id},
        include={"detalles": True, "asesor": True, "cliente": True}
    )
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

# --- UPDATE (Actualizar Pedido y Reemplazar Detalles) ---
@router.put("/pedidos/{pedido_id}", response_model=schemas.Pedido)
async def update_pedido(
    pedido_id: str,
    pedido: schemas.PedidoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        # Verificamos si existe antes de intentar el update complejo
        existente = await db.pedido.find_unique(where={'idPedido': pedido_id})
        if not existente:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        updated_pedido = await db.pedido.update(
            where={'idPedido': pedido_id},
            data={
                "fechaPedido": pedido.fechaPedido,
                "totalPedido": pedido.totalPedido,
                "Status": pedido.Status,
                "updatedBy": current_user.username,
                "asesor": {"connect": {"idAsesor": pedido.idAsesor}},
                "cliente": {"connect": {"idCliente": pedido.idCliente}},
                "detalles": {
                    "delete_many": {}, # Limpia detalles viejos
                    "create": [        # Inserta los nuevos
                        {
                            "idProducto": d.idProducto,
                            "Precio": d.Precio,
                            "Cantidad": d.Cantidad,
                            "Total": d.Precio * d.Cantidad,
                            "createdBy": current_user.username,
                            "updatedBy": current_user.username
                        } for d in pedido.detalles
                    ]
                }
            },
            include={"detalles": True, "asesor": True, "cliente": True}
        )
        return updated_pedido
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar: {str(e)}")

# --- DELETE (Eliminar Pedido y sus Detalles) ---
@router.delete("/pedidos/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pedido(
    pedido_id: str,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user)
):
    try:
        # En Prisma, si configuraste la relación correctamente, 
        # puedes borrar el pedido y los detalles se borrarán si hay cascade,
        # pero para estar seguros lo hacemos manual o Prisma lo maneja por el ID.
        await db.pedido.delete(where={'idPedido': pedido_id})
        return None
    except Exception as e:
        raise HTTPException(status_code=404, detail="Error al eliminar el pedido")