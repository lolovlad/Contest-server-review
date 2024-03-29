#!/bin/bash

alembic upgrade head
python3 /app/create_model.py
gunicorn MainServer.app:app --workers 2 --worker-class  uvicorn.workers.UvicornWorker --bind=0.0.0.0:7000