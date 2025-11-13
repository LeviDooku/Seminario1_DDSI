# mostrar

"""
Muestra por pantalla el contenido de las tablas de la BD
(Punto 3 del seminario)
"""
from __future__ import annotations
from typing import Sequence, Any
import pyodbc

"""
Función imprime_tabla (generada con IA)
Imprime una tabla simple con columnas alineadas

headers: nombres de las columnas
rows: lista de filas, cada una, una secuencia de valores
"""

def imprime_tabla(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    if not rows:
        print("(sin filas)")
        return
    
    col_widths = []
    num_cols = len(headers)

    for col_idx in range(num_cols):
        max_len = len(str(headers[col_idx]))
        for row in rows:
            value = "" if row[col_idx] is None else str(row[col_idx])
            if len(value) > max_len:
                max_len = len(value)
        col_widths.append(max_len)

    # Imprime cabecera
    header_line = " | ".join(
        str(headers[i]).ljust(col_widths[i]) for i in range(num_cols)
    )
    sep_line = "-+-".join("-" * col_widths[i] for i in range(num_cols))

    print(header_line)
    print(sep_line)

    # Imprime filas
    for row in rows:
        line = " | ".join(
            ("" if row[i] is None else str(row[i])).ljust(col_widths[i])
            for i in range(num_cols)
        )
        print(line)

"""
Función mostrar_stock (Generada parcialmente con IA):
Muestra el contenido de la tabla Stock, usando función anterior
"""

def mostrar_stock(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT CPRODUCTO, CANTIDAD
            FROM STOCK
            ORDER BY CPRODUCTO
        """)
        rows = cur.fetchall()

    print("\n=== Tabla STOCK ===")
    if not rows:
        print("(sin filas en Stock)")
    else:
        headers = ["Cproducto", "Cantidad"]
        imprime_tabla(headers, rows)

"""
Función mostrar_pedido (Generada parcialmente con IA):
Muestra el contenido de la tabla Pedido, usando función anterior
"""

def mostrar_pedidos(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                CPEDIDO,
                CCLIENTE,
                TO_CHAR(FECHA_PEDIDO, 'YYYY-MM-DD HH24:MI:SS') AS FECHA_PEDIDO
            FROM PEDIDO
            ORDER BY CPEDIDO
        """)
        rows = cur.fetchall()

    print("\n=== Tabla PEDIDO ===")
    if not rows:
        print("(sin filas en Pedido)")
    else:
        headers = ["Cpedido", "Ccliente", "Fecha_Pedido"]
        imprime_tabla(headers, rows)

"""
Función mostrar_detalles (Generada parcialmente con IA):
Muestra el contenido de la tabla Detalle_Pedido, usando función anterior
"""

def mostrar_detalles(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                CPEDIDO,
                CPRODUCTO,
                CANTIDAD
            FROM DETALLE_PEDIDO
            ORDER BY CPEDIDO, CPRODUCTO
        """)
        rows = cur.fetchall()

    print("\n=== Tabla DETALLE_PEDIDO ===")
    if not rows:
        print("(sin filas en Detalle_Pedido)")
    else:
        headers = ["Cpedido", "Cproducto", "Cantidad"]
        imprime_tabla(headers, rows)

"""
Función mostrar_todo
"""

def mostrar_todo(conn: pyodbc.Connection) -> None:
    print("\n================ CONTENIDO COMPLETO BD ================\n")
    mostrar_stock(conn)
    mostrar_pedidos(conn)
    mostrar_detalles(conn)
    print("\n=======================================================\n")