# debug_conn.py
#
# Script de prueba para:
#  - comprobar pyodbc y el driver
#  - comprobar la conexión y el ping
#  - probar resetea() (DROP + CREATE + INSERT)
#  - probar la lógica de pedidos (iniciar, añadir detalle, eliminar detalles,
#    cancelar y finalizar) SIN GUI, solo en consola.

from db_config import from_env
from db_connection import connect, ping, DBError
from schema import resetea
from mostrar import mostrar_todo

from pedidos_service import (
    iniciar_pedido,
    anadir_detalle,
    eliminar_detalles_pedido,
    cancelar_pedido,
    finalizar_pedido,
    PedidoError,
    ProductoNoExisteError,
    PedidoYaExisteError,
    SinStockError,
)

import pyodbc
import sys


def demo_pedidos(conn: pyodbc.Connection) -> None:
    """
    Ejecuta una serie de pruebas sobre la lógica de pedidos:
      1) Crear un pedido y añadir un detalle (commit).
      2) Crear otro pedido, añadir detalle, eliminar detalles con SAVEPOINT.
      3) Crear otro pedido, añadir detalle y cancelarlo (rollback).
    Todo mostrando el contenido completo de la BD tras cada paso importante.
    """
    print("\n=== DEMO 0: Reset BD inicial ===")
    resetea(conn)
    mostrar_todo(conn)

    # -------------------------------
    # DEMO 1: Pedido que se FINALIZA
    # -------------------------------
    print("\n=== DEMO 1: Pedido que se FINALIZA (COMMIT) ===")
    try:
        cpedido = 1001
        print(f"\n-> Iniciar pedido {cpedido} (cliente 1)")
        iniciar_pedido(conn, cpedido, 1)
        mostrar_todo(conn)

        print("\n-> Añadir detalle: producto 1, cantidad 5")
        anadir_detalle(conn, cpedido, 1, 5)
        mostrar_todo(conn)

        print("\n-> Finalizar pedido (COMMIT)")
        finalizar_pedido(conn)
        mostrar_todo(conn)

    except PedidoError as e:
        print("❌ Error en DEMO 1:", e)
        conn.rollback()

    # -------------------------------
    # DEMO 2: Pedido donde se usan SAVEPOINT + ROLLBACK TO
    # -------------------------------
    print("\n=== DEMO 2: SAVEPOINT + ROLLBACK TO (eliminar detalles) ===")
    try:
        cpedido = 2001
        print(f"\n-> Iniciar pedido {cpedido} (cliente CLI-002)")
        iniciar_pedido(conn, cpedido, 2)
        mostrar_todo(conn)

        print("\n-> Añadir detalle: producto 2, cantidad 3")
        anadir_detalle(conn, cpedido, 2, 3)
        mostrar_todo(conn)

        print("\n-> Añadir otro detalle: producto 3, cantidad 4")
        anadir_detalle(conn, cpedido, 3, 4)
        mostrar_todo(conn)

        print("\n-> Eliminar TODOS los detalles (ROLLBACK TO SAVEPOINT)")
        eliminar_detalles_pedido(conn)
        mostrar_todo(conn)

        print("\n-> Añadir detalle de nuevo: producto 2, cantidad 1")
        anadir_detalle(conn, cpedido, 2, 1)
        mostrar_todo(conn)

        print("\n-> Finalizar pedido (COMMIT)")
        finalizar_pedido(conn)
        mostrar_todo(conn)

    except PedidoError as e:
        print("❌ Error en DEMO 2:", e)
        conn.rollback()

    # -------------------------------
    # DEMO 3: Pedido que se CANCELA
    # -------------------------------
    print("\n=== DEMO 3: Pedido que se CANCELA (ROLLBACK) ===")
    try:
        cpedido = 3001
        print(f"\n-> Iniciar pedido {cpedido} (cliente CLI-003)")
        iniciar_pedido(conn, cpedido, 3)
        mostrar_todo(conn)

        print("\n-> Añadir detalle: producto 4, cantidad 2")
        anadir_detalle(conn, cpedido, 4, 2)
        mostrar_todo(conn)

        print("\n-> Cancelar pedido (ROLLBACK)")
        cancelar_pedido(conn)
        mostrar_todo(conn)

    except PedidoError as e:
        print("❌ Error en DEMO 3:", e)
        conn.rollback()

    # -------------------------------
    # DEMO 4: Probar error de stock
    # -------------------------------
    print("\n=== DEMO 4: Error de stock (SinStockError) ===")
    try:
        cpedido = 4001
        print(f"\n-> Iniciar pedido {cpedido} (cliente CLI-004)")
        iniciar_pedido(conn, cpedido, 4)
        mostrar_todo(conn)

        print("\n-> Intentar añadir detalle con más cantidad de la disponible")
        # Suponiendo que el producto 1 tiene stock limitado en tu tabla inicial
        anadir_detalle(conn, cpedido, 1, 999999)

    except SinStockError as e:
        print("✅ Se ha capturado correctamente SinStockError:")
        print("   ", e)
        # No hacemos commit: deshacemos todo el pedido
        cancelar_pedido(conn)
        mostrar_todo(conn)

    except PedidoError as e:
        print("❌ Otro error de pedidos en DEMO 4:", e)
        conn.rollback()

    print("\n=== FIN DE DEMOS ===")


def main():
    try:
        print("=== Comprobando pyodbc y configuración ===")
        print("pyodbc.drivers():", pyodbc.drivers())

        cfg = from_env()
        safe = getattr(cfg, "odbc_conn_str_safe", lambda: "<no safe method>")()
        print("ODBC conn str (safe):", safe)

        print("\n=== Probando conexión y ping ===")
        conn = connect(cfg)
        print("✅ Conexión creada")

        usuario, ahora = ping(conn)
        print(f"✅ Ping OK | Usuario: {usuario} | SYSDATE: {ahora}")

        # Llamamos a las demos de pedidos
        demo_pedidos(conn)

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
