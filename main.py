from fastapi import FastAPI
from app.routes import auth
from app.routes.asesores import router as asesores_router
from app.routes.productos import router as productos_router
from app.routes.clientes import router as clientes_router
from app.routes.pedidos import router as pedidos_router
from app.routes.detalle_pedidos import router as detalle_pedidos_router
from fastapi.middleware.cors import CORSMiddleware # Importación necesaria

import os
import time

# Configuración de zona horaria
os.environ['TZ'] = 'America/Caracas'
if hasattr(time, 'tzset'):
    time.tzset()
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier URL
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Registro de rutas (routers)
app.include_router(auth.router)
app.include_router(asesores_router, tags=["Asesores"])
app.include_router(productos_router, tags=["Productos"])
app.include_router(clientes_router, tags=["Clientes"])
app.include_router(pedidos_router, tags=["Pedidos"])
app.include_router(detalle_pedidos_router, tags=["DetallePedidos"])