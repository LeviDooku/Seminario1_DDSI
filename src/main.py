# main.py
#
# Punto de entrada de la aplicación:
#  - carga config
#  - abre conexión
#  - lanza la GUI
#  - cierra conexión al salir

from db_config import from_env
from db_connection import connect, DBError
from GUI import iniciar_gui

import pyodbc
import sys

def main():
    try:
        cfg = from_env()
        conn = connect(cfg)
        print("✅ Conexión creada. Lanzando GUI...")

        iniciar_gui(conn)   # aquí se bloquea hasta que cierres la ventana

        conn.close()
        print("✅ Conexión cerrada. Saliendo de la aplicación.")
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