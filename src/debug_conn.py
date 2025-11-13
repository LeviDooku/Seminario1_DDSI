# debug_conn.py
#
# Script de prueba para:
#  - comprobar pyodbc y el driver
#  - comprobar la conexión y el ping
#  - probar resetea() (DROP + CREATE + INSERT)
#  - mostrar el contenido completo de las tablas mediante mostrar_todo()

from db_config import from_env
from db_connection import connect, ping, DBError
from schema import resetea
from mostrar import mostrar_todo

import pyodbc
import sys


def main():
    try:
        print("=== Comprobando pyodbc y configuración ===")
        print("pyodbc.drivers():", pyodbc.drivers())

        cfg = from_env()
        # muestra el conn_str sin contraseña para diagnosticar
        safe = getattr(cfg, "odbc_conn_str_safe", lambda: "<no safe method>")()
        print("ODBC conn str (safe):", safe)

        print("\n=== Probando conexión y ping ===")
        conn = connect(cfg)  # si falla, lanzará DBError
        print("✅ Conexión creada")

        usuario, ahora = ping(conn)
        print(f"✅ Ping OK | Usuario: {usuario} | SYSDATE: {ahora}")

        print("\n=== Probando resetea() (DROP + CREATE + INSERT) ===")
        resetea(conn)
        print("✅ Esquema recreado e inicializado")

        print("\n=== Mostrando contenido completo de la BD ===")
        mostrar_todo(conn)

        conn.close()
        print("\n✅ Conexión cerrada")
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
