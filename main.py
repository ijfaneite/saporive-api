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

# --- CONFIGURACIÓN DE CORS ---
#Lista de orígenes permitidos
origins = [
    "http://localhost:3000",
    # Esta es la URL de tu entorno de Cloud Workstations que aparece en el error:
    "https://6000-firebase-studio-1768458030600.cluster-j6d3cbsvdbe5uxnhqrfzzeyj7i.cloudworkstations.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Permite los orígenes definidos arriba
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Permite todos los encabezados (Authorization, Content-Type, etc.)
)
# -----------------------------

# Registro de rutas (routers)
app.include_router(auth.router)
app.include_router(asesores_router, tags=["Asesores"])
app.include_router(productos_router, tags=["Productos"])
app.include_router(clientes_router, tags=["Clientes"])
app.include_router(pedidos_router, tags=["Pedidos"])
app.include_router(detalle_pedidos_router, tags=["DetallePedidos"])