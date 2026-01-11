from fastapi import APIRouter, HTTPException, status, Depends
from prisma import Prisma
from app import schemas
from .auth import get_current_active_user

router = APIRouter()

# Dependency to get a Prisma client instance
async def get_prisma_client():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


@router.post("/productos/", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
async def create_producto(
    producto: schemas.ProductoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        created_producto = await db.producto.create(data={
            "Producto": producto.Producto,
            "Precio": producto.Precio,
            "createdBy": current_user.username,
            "updatedBy": current_user.username
        })
        return created_producto
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/productos/", response_model=list[schemas.Producto])
async def read_productos(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    productos = await db.producto.find_many()
    return productos


@router.get("/productos/{producto_id}", response_model=schemas.Producto)
async def read_producto(
    producto_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    producto = await db.producto.find_unique(where={'idProducto': producto_id})
    if producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found")
    return producto


@router.put("/productos/{producto_id}", response_model=schemas.Producto)
async def update_producto(
    producto_id: str,
    producto: schemas.ProductoCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        updated_producto = await db.producto.update(
            where={'idProducto': producto_id},
            data={
                'Producto': producto.Producto,
                'Precio': producto.Precio,
                'updatedBy': current_user.username
            }
        )
        return updated_producto
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found or error during update")


@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(
    producto_id: str,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Prisma = Depends(get_prisma_client)
):
    try:
        await db.producto.delete(where={'idProducto': producto_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found or error during delete")
