import asyncio
import pandas as pd
from prisma import Prisma
from datetime import datetime

async def import_clientes():
    db = Prisma()
    await db.connect()

    # Leer el CSV
    df = pd.read_csv('Clientes.csv')
    
    # Limpiar posibles valores nulos en Zona
    df['zona'] = df['zona'].fillna('SIN ZONA')

    print(f"Cargando {len(df)} clientes...")

    for index, row in df.iterrows():
        try:
            await db.cliente.upsert(
                where={
                    'Rif': str(row['rif'])
                },
                data={
                    'create': {
                        'idCliente': str(row['idCliente']),
                        'Rif': str(row['rif']),
                        'Cliente': str(row['cliente']),
                        'Zona': str(row['zona']),
                        'idAsesor': str(row['idAsesor']),
                        'createdBy': 'ijfaneite',
                        'updatedBy': 'ijfaneite',
                    },
                    'update': {
                        'Cliente': str(row['cliente']),
                        'Zona': str(row['zona']),
                        'idAsesor': str(row['idAsesor']),
                        'updatedBy': 'ijfaneite',
                    }
                }
            )
        except Exception as e:
            print(f"Error en fila {index} (Rif: {row['rif']}): {e}")

    await db.disconnect()
    print("Importación completada.")

if __name__ == '__main__':
    asyncio.run(import_clientes())