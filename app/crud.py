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

# ========================= EMPLEADOS =========================
def fetch_all_empleados() -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_empleado, nombre, especialidad, telefono, email FROM empleados;")
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def insert_empleado(nombre: str, especialidad: str, telefono: str | None = None, email: str | None = None) -> int:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO empleados (nombre, especialidad, telefono, email) VALUES (%s, %s, %s, %s)",
                (nombre, especialidad, telefono, email)
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_empleado_by_id(empleado_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_empleado, nombre, especialidad, telefono, email FROM empleados WHERE id_empleado=%s", (empleado_id,))
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_empleado(empleado_id: int, nombre: str, especialidad: str, telefono: str | None = None, email: str | None = None) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE empleados SET nombre=%s, especialidad=%s, telefono=%s, email=%s WHERE id_empleado=%s",
                (nombre, especialidad, telefono, email, empleado_id)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_empleado(empleado_id: int) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM empleados WHERE id_empleado=%s", (empleado_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

# ========================= SERVICIOS =========================
def fetch_all_servicios() -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_servicio, nombre, precio FROM servicios;")
            return cast(List[Dict[str, Any]], cur.fetchall())
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def insert_servicio(nombre: str, precio: float) -> int:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO servicios (nombre, precio) VALUES (%s, %s)", (nombre, precio))
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_servicio_by_id(servicio_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_servicio, nombre, precio FROM servicios WHERE id_servicio=%s", (servicio_id,))
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_servicio(servicio_id: int, nombre: str, precio: float) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE servicios SET nombre=%s, precio=%s WHERE id_servicio=%s", (nombre, precio, servicio_id))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_servicio(servicio_id: int) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM servicios WHERE id_servicio=%s", (servicio_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

# ========================= CITAS =========================
def fetch_all_citas() -> List[Dict[str, Any]]:
    """
    Retorna todas las citas, uniendo cliente, empleado y servicio para mostrar nombres.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("""
                SELECT c.id_cita, cl.nombre AS cliente_nombre, e.nombre AS empleado_nombre,
                       s.nombre AS servicio_nombre, c.fecha
                FROM citas c
                JOIN clientes cl ON c.id_cliente = cl.id_cliente
                JOIN empleados e ON c.id_empleado = e.id_empleado
                JOIN servicios s ON c.id_servicio = s.id_servicio
                ORDER BY c.fecha DESC;
            """)
            return cast(List[Dict[str, Any]], cur.fetchall())
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def insert_cita(id_cliente: int, id_empleado: int, id_servicio: int, fecha: str) -> int:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO citas (id_cliente, id_empleado, id_servicio, fecha) VALUES (%s,%s,%s,%s)",
                (id_cliente, id_empleado, id_servicio, fecha)
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_cita_by_id(cita_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT * FROM citas WHERE id_cita=%s", (cita_id,))
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def update_cita(cita_id: int, id_cliente: int, id_empleado: int, id_servicio: int, fecha: str) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE citas SET id_cliente=%s, id_empleado=%s, id_servicio=%s, fecha=%s WHERE id_cita=%s",
                (id_cliente, id_empleado, id_servicio, fecha, cita_id)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def delete_cita(cita_id: int) -> bool:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM citas WHERE id_cita=%s", (cita_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()
