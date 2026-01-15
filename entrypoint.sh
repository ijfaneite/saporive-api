#!/bin/bash

# Activar zona horaria
export TZ="America/Caracas"

echo "Generando cliente Prisma..."
prisma generate

echo "Fetch Cliente..."
prisma py fetch
 
echo "Sincronizando base de datos (db push)..."
python -m prisma db push

echo "Ejecutando migraciones..."
# Usamos deploy en lugar de dev para entornos de producción/docker
prisma migrate deploy || echo "No hay migraciones nuevas o ya se aplicaron."

echo "Iniciando servidor con Gunicorn..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app