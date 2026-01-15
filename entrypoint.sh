#!/bin/bash
echo "Instalando pip install pwdlib[argon2]"


# Activar zona horaria
export TZ="America/Caracas"

echo "Generando cliente Prisma..."
prisma generate

echo "Fetch Cliente..."
prisma py fetch
 
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

echo "Configuración de Prisma completada."

echo "Iniciando servidor con Gunicorn..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app