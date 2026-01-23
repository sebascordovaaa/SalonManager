import mysql.connector
import os                     # <— importado os para leer variables de entorno          
from dotenv import load_dotenv


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),        # <— corregidos nombres
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "peluqueria_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )
