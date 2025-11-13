# db_connection

from __future__ import annotations
from db_config import DBConfig
import pyodbc

class DBError(RuntimeError):
    """
    Error genérico de acceso a BD
    """
def assert_driver_avaliable(cfg: DBConfig) -> None:
    """
    Falla si el driver OCDB indicado no está instalado.
    """
    drivers = set(pyodbc.drivers())
    if cfg.driver not in drivers:
        raise DBError(
            f"Driver ODBC no encontrado: '{cfg.driver}'. "
            f"Drivers instalados: {sorted:(drivers)}"
        )
    
def connect(cfg: DBConfig) -> pyodbc.Connection:
    """
    Devuelve una conexión válida o lanza DBError.
    Nunca retorna None.
    """
    assert_driver_avaliable(cfg)
    try:
        conn = pyodbc.connect(cfg.odbc_convertir, autocommit=cfg.autocommit)
        if conn is None:  # por si algún driver devuelve None (no debería)
            raise DBError("pyodbc.connect devolvió None (conexión inválida).")
        return conn
    except pyodbc.Error as e:
        # oculta la contraseña si lo imprimes
        try:
            safe = cfg.odbc_conn_str_safe()
        except Exception:
            safe = "<conn_str oculto>"
        raise DBError(f"Error conectando a Oracle con: {safe}\n{e}") from e
        
def ping(conn: pyodbc.Connection) -> tuple[str, str]:
    """
    Devuelve (usuario, fecha_hora). Requiere una conexión válida.
    """
    if conn is None:
        raise DBError("Conexión None recibida en ping(). Revisa connect().")
    with conn.cursor() as cur:
        cur.execute("SELECT user, TO_CHAR(SYSDATE,'YYYY-MM-DD HH24:MI:SS') FROM dual")
        return cur.fetchone()
