echo "Configuración de Prisma completada."
echo "Iniciando servidor con Gunicorn..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app