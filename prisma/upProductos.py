import asyncio
import pandas as pd
from prisma import Prisma

async def import_productos():
    db = Prisma()
    await db.connect()

    # Leer el CSV
    df = pd.read_csv('productos.csv')
    
    print(f"Cargando {len(df)} productos...")

    for index, row in df.iterrows():
        try:
            # Convertimos precio a float por si viene como string
            precio_float = float(row['precio'])
            
            await db.producto.upsert(
                where={
                    'idProducto': str(row['idProducto'])
                },
                data={
                    'create': {
                        'idProducto': str(row['idProducto']),
                        'Producto': str(row['producto']),
                        'Precio': precio_float,
                        'createdBy': 'ijfaneite',
                        'updatedBy': 'ijfaneite',
                    },
                    'update': {
                        'Producto': str(row['producto']),
                        'Precio': precio_float,
                        'updatedBy': 'ijfaneite',
                    }
                }
            )
        except Exception as e:
            print(f"Error en producto {row['idProducto']}: {e}")

    await db.disconnect()
    print("Productos importados exitosamente.")

if __name__ == '__main__':
    asyncio.run(import_productos())