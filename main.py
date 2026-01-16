from fastapi import FastAPI
from app.routes import auth, empresas  # Importamos el nuevo router de empresas
from app.routes.asesores import router as asesores_router
from app.routes.productos import router as productos_router
from app.routes.clientes import router as clientes_router
from app.routes.pedidos import router as pedidos_router
from app.routes.detalle_pedidos import router as detalle_pedidos_router
from fastapi.middleware.cors import CORSMiddleware

import os
import time

# Configuración de zona horaria para Venezuela 
os.environ['TZ'] = 'America/Caracas'
if hasattr(time, 'tzset'):
    time.tzset()
    
app = FastAPI()

# Configuración de CORS permisiva para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Registro de rutas (routers)
app.include_router(auth.router)
app.include_router(empresas.router, tags=["Empresas"]) # Registro de la nueva ruta de Empresas
app.include_router(asesores_router, tags=["Asesores"])
app.include_router(productos_router, tags=["Productos"])
app.include_router(clientes_router, tags=["Clientes"])
app.include_router(pedidos_router, tags=["Pedidos"])
app.include_router(detalle_pedidos_router, tags=["DetallePedidos"])