#!/bin/sh

set -e

echo "Odpalamy apkę"

echo $ENV_TYPE

echo "Jedziemy"



# exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
exec python3 ai_devs/main.py
