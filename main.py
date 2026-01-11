from fastapi import FastAPI
from app.routes import auth
from app.routes.asesores import router as asesores_router
from app.routes.productos import router as productos_router
from app.routes.clientes import router as clientes_router
from app.routes.pedidos import router as pedidos_router
from app.routes.detalle_pedidos import router as detalle_pedidos_router # Added import

app = FastAPI()

app.include_router(auth.router)
app.include_router(asesores_router, tags=["Asesores"])
app.include_router(productos_router, tags=["Productos"])
app.include_router(clientes_router, tags=["Clientes"])
app.include_router(pedidos_router, tags=["Pedidos"])
app.include_router(detalle_pedidos_router, tags=["DetallePedidos"]) # Added include_router for DetallePedidos