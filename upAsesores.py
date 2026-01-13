import asyncio
import pandas as pd
from prisma import Prisma
import uuid

async def import_asesores():
    db = Prisma()
    await db.connect()

    # Leer el CSV
    df = pd.read_csv('asesores.csv')
    
    # Eliminar duplicados en el DataFrame basados en CodAsesor para evitar errores
    df = df.drop_duplicates(subset=['idAsesor'])

    print(f"Cargando {len(df)} asesores únicos...")

    for index, row in df.iterrows():
        try:
            await db.asesor.upsert(
                where={
                    'idAsesor': str(row['idAsesor'])
                },
                data={
                    'create': {
                        'idAsesor': str(row['idAsesor']),
                        'Asesor': str(row['asesor']),
                        'createdBy': 'ijfaneite',
                        'updatedBy': 'ijfaneite',
                    },
                    'update': {
                        'Asesor': str(row['asesor']),
                        'updatedBy': 'ijfaneite',
                    }
                }
            )
        except Exception as e:
            print(f"Error en asesor {row['idAsesor']}: {e}")

    await db.disconnect()
    print("Asesores importados exitosamente.")

if __name__ == '__main__':
    asyncio.run(import_asesores())