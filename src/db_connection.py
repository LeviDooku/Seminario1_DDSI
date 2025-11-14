# db_connection

"""
Gestiona la conexión a la BD usando pyodbc

https://github.com/mkleehammer/pyodbc/wiki
"""

from __future__ import annotations
from db_config import DBConfig
import pyodbc

"""
Clase DBError:
Crea un tipo de error personalizado específico para problemas de BD
Útil para capturar errores de este aspecto
"""

class DBError(RuntimeError):
    pass

"""
Función comprobar_driver:
Comprueba si el driver odbc requerido por el objeto DBconfig está instalado
y en uso
"""
def comprobar_driver(cfg: DBConfig) -> None:
    drivers = set(pyodbc.drivers())
    if cfg.driver not in drivers:
        raise DBError(
            f"Driver ODBC no encontrado: '{cfg.driver}'. "
            f"Drivers instalados: {sorted(drivers)}"
        )

"""
Función connect:
Verifica que el driver esté disponible y establece la conexión
Además, valida el resultado (que no sea none)
"""
def connect(cfg: DBConfig) -> pyodbc.Connection:
    comprobar_driver(cfg)
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
        
"""
Función ping:
Valida la conexión y muestra usuario y momento en el que inició sesión    
"""
def ping(conn: pyodbc.Connection) -> tuple[str, str]:
    if conn is None:
        raise DBError("Conexión None recibida en ping(). Revisa connect().")
    with conn.cursor() as cur:
        cur.execute("SELECT user, TO_CHAR(SYSDATE,'YYYY-MM-DD HH24:MI:SS') FROM dual")
        return cur.fetchone()
