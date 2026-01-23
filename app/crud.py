from typing import List, Dict, Any, cast
from app.database import get_connection
from mysql.connector.cursor import MySQLCursorDict

# ========================= CLIENTES =========================
def fetch_all_clientes() -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT id_cliente, nombre, email, telefono, fecha_registro FROM clientes;"
            )
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def insert_cliente(nombre: str, telefono: str, email: str | None = None) -> int:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO clientes (nombre, telefono, email)
                VALUES (%s, %s, %s)
                """,
                (nombre, telefono, email)
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_cliente_by_id(cliente_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT id_cliente, nombre, email, telefono, fecha_registro FROM clientes WHERE id_cliente = %s",
                (cliente_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def update_cliente(cliente_id: int, nombre: str, email: str, telefono: str | None = None) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE clientes 
                SET nombre = %s, email = %s, telefono = %s
                WHERE id_cliente = %s
                """,
                (nombre, email, telefono, cliente_id)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_cliente(cliente_id: int) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()
