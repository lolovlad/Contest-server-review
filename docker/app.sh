#!/bin/bash

alembic upgrade head
python3 /app/create_model.py
python3 /app/run_server.py