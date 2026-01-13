#!/bin/bash



source .venv/bin/activate

# Forzar la zona horaria a nivel de sistema para este proceso
export TZ="America/Caracas"

# Tu comando de siempre para correr el server
uvicorn main:app --host localhost --port 8000 --reload
