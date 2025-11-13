# debug_conn.py

from db_config import from_env
from db_connection import connect, ping, DBError
import pyodbc
import os
import sys

def main():
    try:
        print("pyodbc.drivers():", pyodbc.drivers())
        cfg = from_env()
        # muestra el conn_str sin contraseña para diagnosticar
        safe = getattr(cfg, "odbc_conn_str_safe", lambda: "<no safe method>")()
        print("ODBC conn str (safe):", safe)

        conn = connect(cfg)  # si falla, lanzará DBError
        print("✅ Conexión creada")
        usuario, ahora = ping(conn)
        print(f"✅ Ping OK | Usuario: {usuario} | SYSDATE: {ahora}")
        conn.close()
        print("✅ Conexión cerrada")
        return 0

    except DBError as e:
        print("❌ DBError:", e, file=sys.stderr)
        return 2
    except pyodbc.Error as e:
        print("❌ pyodbc.Error:", e, file=sys.stderr)
        return 3
    except Exception as e:
        print("❌ Error general:", e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
