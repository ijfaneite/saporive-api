#!/bin/bash

# Activar el entorno virtual
rm -rf .venv ~/.cache/pip ~/.cache/prisma-python
python3.13 -m venv .venv 
source .venv/bin/activate

pip install --upgrade pip setuptools wheel && pip install --no-cache-dir  -U -r requirements.txt && prisma generate && prisma py fetch && prisma db push

echo "Ejecutando prisma generate..."
python -m prisma db push

if [ $? -eq 0 ]; then
  echo "prisma generate completado exitosamente."
else
  echo "Error durante prisma generate. Por favor, revisa la salida anterior."
  exit 1
fi

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

# Forzar la zona horaria a nivel de sistema para este proceso
export TZ="America/Caracas"

# Tu comando de siempre para correr el server
#uvicorn main:app --host localhost --port 8000 --reload
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app