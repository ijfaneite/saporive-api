#!/bin/bash
echo "INSTALAR TODAS LAS DEPENDENCIAS...."
pip install -r requirements.txt

# Activar zona horaria
export TZ="America/Caracas"

echo "Fetch Cliente... VE A LA FERRETERIA A COMPRAR LOS MATERIALES"
prisma py fetch

echo "Generando cliente Prisma... CONSTRUYE LA CASA"
prisma generate

echo "Sincronizando base de datos (db push)..."
python -m prisma db push

#echo "Ejecutando migraciones..."
# Usamos deploy en lugar de dev para entornos de producción/docker
#prisma migrate deploy || echo "No hay migraciones nuevas o ya se aplicaron."

# Define un nombre para la migración. Puedes cambiarlo si lo deseas.
MIGRATION_NAME="db"

echo "Ejecutando prisma migrate dev --name ${MIGRATION_NAME}..."
prisma migrate dev --name "${MIGRATION_NAME}"

if [ $? -eq 0 ]; then
  echo "prisma migrate dev completado exitosamente."
else
  echo "Error durante prisma migrate dev. Por favor, revisa la salida anterior."
  echo "Asegúrate de que tu base de datos esté accesible y OpenSSL configurado correctamente."
  exit 1
fi