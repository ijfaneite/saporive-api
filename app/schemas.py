from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional # Asegúrate de tener estas importaciones


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):  # Assuming this is the schema for the User model (from a previous step)
    username: str
    # Add timestamps for the User model
    createdAt: datetime
    updatedAt: datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class EmpresaBase(BaseModel):
    RazonSocial: str
    idPedido: int
    idRecibo: int # Debe ser igual al schema.prisma 

class EmpresaUpdatePedidos(BaseModel):
    idPedido: int
    
class Empresa(EmpresaBase):
    idEmpresa: int
    class Config:
        from_attributes = True


class AsesorBase(BaseModel):
    Asesor: str
    # Add timestamps and audit fields to AsesorBase
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    createdBy: str | None = None
    updatedBy: str | None = None


class Asesor(AsesorBase):
    idAsesor: str   # Prisma returns 'id' by default for primary keys

    class Config:
        from_attributes = True

class AsesorCreate(Asesor):
    # These fields are set automatically by the backend, so they should not be required on creation
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

class ProductoBase(BaseModel):
    Producto: str
    Precio: float
    # Add timestamps and audit fields to ProductoBase
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    createdBy: str | None = None
    updatedBy: str | None = None


class ProductoCreate(ProductoBase):
    # These fields are set automatically by the backend, so they should not be required on creation
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)


class Producto(ProductoBase):
    idProducto: str 

    class Config:
        from_attributes = True


class ClienteBase(BaseModel):
    Zona: str
    idAsesor: str
    asesor: Asesor | None = None  # This will be the related Asesor object

    # Add timestamps and audit fields to ClienteBase
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    createdBy: str | None = None
    updatedBy: str | None = None


class ClienteCreate(ClienteBase):
    # These fields are set automatically by the backend, so they should not be required on creation
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)


class Cliente(ClienteBase):
    idCliente: str 
    Cliente: str
    Rif: str

    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    idPedido: str 
    idEmpresa: int
    fechaPedido: datetime
    totalPedido: float
    idAsesor: str
    idCliente: str
    Status: str

class PedidoCreate(PedidoBase):
    # Campos que el backend genera automáticamente
    createdAt: Optional[datetime] = Field(None, exclude=True)
    updatedAt: Optional[datetime] = Field(None, exclude=True)
    createdBy: Optional[str] = Field(None, exclude=True)
    updatedBy: Optional[str] = Field(None, exclude=True)

class Pedido(PedidoBase):
    # Relaciones (Usamos strings para evitar errores de referencia circular)
    asesor: Optional["Asesor"] = None
    cliente: Optional["Cliente"] = None
    # CORRECCIÓN: Un pedido ahora contiene una lista de sus detalles
    detalles: List["DetallePedido"] = [] 
    
    # Campos de auditoría obligatorios en la respuesta
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str

    class Config:
        from_attributes = True


class DetallePedidoBase(BaseModel):
    idPedido: str
    idProducto: str
    Precio: float
    Cantidad: int

class DetallePedidoCreate(DetallePedidoBase):
    Total: Optional[float] = Field(None, exclude=True)
    createdAt: Optional[datetime] = Field(None, exclude=True)
    updatedAt: Optional[datetime] = Field(None, exclude=True)
    createdBy: Optional[str] = Field(None, exclude=True)
    updatedBy: Optional[str] = Field(None, exclude=True)

class DetallePedido(DetallePedidoBase):
    id: str # UUID generado por Prisma
    idPedido: str
    Total: float
    # Relaciones
    pedido: Optional["Pedido"] = None
    producto: Optional["Producto"] = None
    
    # Campos de auditoría
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str

    class Config:
        from_attributes = True

# Al final del archivo schemas.py, es bueno llamar a esto para resolver 
# las referencias circulares de las relaciones (strings "Pedido", etc.)
Pedido.model_rebuild()
DetallePedido.model_rebuild()