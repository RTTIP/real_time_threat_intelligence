# app/config.py
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db-1.c5o4k2em6pvs.us-east-1.rds.amazonaws.com"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres123"),
    "database": os.getenv("DB_NAME", "postgres")
}


