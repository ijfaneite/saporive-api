import asyncio
from prisma import Prisma

async def insertar_empresa():
    # 1. Instanciar el cliente de Prisma
    db = Prisma()
    
    # 2. Conectar a la base de datos
    await db.connect()

    try:
        # 3. Realizar la inserción (Create)
        # Nota: 'idEmpresa' no se envía porque es autoincremental
        nueva_empresa = await db.empresa.create(
            data={
                'RazonSocial': 'Sapori, CA',
                'idPedido': 1,
                'idRecibo': 1
            }
        )
        
        print(f"✅ Registro insertado con éxito. ID generado: {nueva_empresa.idEmpresa}")

    except Exception as e:
        print(f"❌ Error al insertar: {e}")
        
    finally:
        # 4. Desconectar siempre al finalizar
        await db.disconnect()

# Ejecutar la función asíncrona
if __name__ == "__main__":
    asyncio.run(insertar_empresa())