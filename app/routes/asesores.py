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


@router.post("/asesores/", response_model=schemas.Asesor, status_code=status.HTTP_201_CREATED)
async def create_asesor(
    asesor: schemas.AsesorCreate,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user) # Add dependency
):
    try:
        created_asesor = await db.asesor.create(data={
            "Asesor": asesor.Asesor,
            "createdBy": current_user.username, # Set createdBy
            "updatedBy": current_user.username  # Set updatedBy initially
        })
        return created_asesor
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/asesores/", response_model=list[schemas.Asesor])
async def read_asesores(
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user) # Add dependency
):
    asesores = await db.asesor.find_many()
    return asesores


@router.get("/asesores/{asesor_id}", response_model=schemas.Asesor)
async def read_asesor(
    asesor_id: str,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user) # Add dependency
):
    asesor = await db.asesor.find_unique(where={'idAsesor': asesor_id})
    if asesor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asesor not found")
    return asesor


@router.put("/asesores/{asesor_id}", response_model=schemas.Asesor)
async def update_asesor(
    asesor_id: str,
    asesor: schemas.AsesorCreate,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user) # Add dependency
):
    try:
        updated_asesor = await db.asesor.update(
            where={'idAsesor': asesor_id},
            data={
                'Asesor': asesor.Asesor,
                "updatedBy": current_user.username # Set updatedBy
            }
        )
        return updated_asesor
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asesor not found or error during update")


@router.delete("/asesores/{asesor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asesor(
    asesor_id: str,
    db: Prisma = Depends(get_prisma_client),
    current_user: schemas.User = Depends(get_current_active_user) # Add dependency
):
    try:
        await db.asesor.delete(where={'idAsesor': asesor_id})
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asesor not found or error during delete")