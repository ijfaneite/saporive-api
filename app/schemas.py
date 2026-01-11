from pydantic import BaseModel, Field
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):  # Assuming this is the schema for the User model (from a previous step)
    username: str
    # Add timestamps for the User model
    createdAt: datetime
    updatedAt: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AsesorBase(BaseModel):
    Asesor: str
    # Add timestamps and audit fields to AsesorBase
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    createdBy: str | None = None
    updatedBy: str | None = None


class AsesorCreate(AsesorBase):
    # These fields are set automatically by the backend, so they should not be required on creation
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)


class Asesor(AsesorBase):
    idAsesor: str = Field(..., alias='id')  # Prisma returns 'id' by default for primary keys

    class Config:
        from_attributes = True


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
    idProducto: str = Field(..., alias='id')

    class Config:
        from_attributes = True


class ClienteBase(BaseModel):
    Rif: str
    Cliente: str
    Zona: str
    idAsesor: str
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
    idCliente: str = Field(..., alias='id')
    asesor: Asesor | None = None  # This will be the related Asesor object

    class Config:
        from_attributes = True


class PedidoBase(BaseModel):
    fechaPedido: datetime
    totalPedido: float
    idAsesor: str
    idCliente: str # Added idCliente to PedidoBase
    Status: str


class PedidoCreate(PedidoBase):
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)


class Pedido(PedidoBase):
    idPedido: str = Field(..., alias='id')
    asesor: Asesor | None = None
    cliente: Cliente | None = None # Added cliente to Pedido
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
    # Total will be calculated by the backend


class DetallePedidoCreate(DetallePedidoBase):
    # Exclude auto-generated fields from creation input
    Total: float = Field(None, exclude=True)
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)


class DetallePedido(DetallePedidoBase):
    id: str = Field(..., alias='id')
    Total: float # Total is included in the response model
    pedido: Pedido | None = None
    producto: Producto | None = None
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str

    class Config:
        from_attributes = True