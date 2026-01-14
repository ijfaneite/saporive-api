FROM python:3.11-slim

# Evitar archivos .pyc y habilitar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="America/Caracas"

WORKDIR /saporive-api

# Instalamos dependencias del sistema esenciales para Prisma y Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    openssl \
    direnv \
    && rm -rf /var/lib/apt/lists/*

# Instalación de dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "pwdlib[bcrypt]"

# Copiamos el resto del código
COPY . .

# Exponemos el puerto
EXPOSE 8000

# Usamos el script de entrada que creamos
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]