from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List, Optional

# --- USUARIO ---
class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    createdAt: datetime
    updatedAt: datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- EMPRESA ---
class EmpresaBase(BaseModel):
    RazonSocial: str
    idPedido: int
    idRecibo: int

class Empresa(EmpresaBase):
    idEmpresa: int
    class Config:
        from_attributes = True

# --- ASESOR ---
class AsesorBase(BaseModel):
    Asesor: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None

class Asesor(AsesorBase):
    idAsesor: str
    class Config:
        from_attributes = True

class AsesorCreate(Asesor):
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

# --- PRODUCTO ---
class ProductoBase(BaseModel):
    Producto: str
    Precio: float
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None

class Producto(ProductoBase):
    idProducto: str
    class Config:
        from_attributes = True

class ProductoCreate(ProductoBase):
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

# --- CLIENTE ---
class ClienteBase(BaseModel):
    Cliente: str
    Rif: str
    Zona: str
    idAsesor: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None

class Cliente(ClienteBase):
    idCliente: str
    asesor: Optional[Asesor] = None
    class Config:
        from_attributes = True

class ClienteCreate(ClienteBase):
    idCliente: str
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

# --- DETALLE PEDIDO ---
class DetallePedidoBase(BaseModel):
    idProducto: str
    Precio: float
    Cantidad: int

class DetallePedidoCreate(DetallePedidoBase):
    # Campos que el backend calcula o genera
    Total: float = Field(None, exclude=True)
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

class DetallePedido(DetallePedidoBase):
    id: str
    idPedido: str
    Total: float
    # Relación opcional para evitar recursión infinita
    producto: Optional[Producto] = None
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str

    class Config:
        from_attributes = True

# --- PEDIDO ---
class PedidoBase(BaseModel):
    idPedido: str 
    idEmpresa: int
    fechaPedido: datetime
    totalPedido: float
    idAsesor: str
    idCliente: str
    Status: str

class PedidoCreate(PedidoBase):
    # CLAVE: Recibe la lista de detalles desde el frontend
    detalles: List[DetallePedidoBase]
    createdAt: datetime = Field(None, exclude=True)
    updatedAt: datetime = Field(None, exclude=True)
    createdBy: str = Field(None, exclude=True)
    updatedBy: str = Field(None, exclude=True)

class Pedido(PedidoBase):
    asesor: Optional[Asesor] = None
    cliente: Optional[Cliente] = None
    # CLAVE: Devuelve la lista completa de detalles
    detalles: List[DetallePedido] = []
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str

    class Config:
        from_attributes = True


class EmpresaUpdatePedidos(BaseModel):
    idPedido: int
    
# --- RECONSTRUCCIÓN PARA REFERENCIAS CRUZADAS ---
# Esto permite que Pedido reconozca a DetallePedido aunque estén en el mismo archivo
Pedido.model_rebuild()
DetallePedido.model_rebuild()