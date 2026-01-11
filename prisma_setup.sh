#!/bin/bash

# Activar el entorno virtual
source .venv/bin/activate

echo "Ejecutando prisma generate..."
prisma generate

if [ $? -eq 0 ]; then
  echo "prisma generate completado exitosamente."
else
  echo "Error durante prisma generate. Por favor, revisa la salida anterior."
  exit 1
fi

# Define un nombre para la migración. Puedes cambiarlo si lo deseas.
MIGRATION_NAME="setup_all_models"

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