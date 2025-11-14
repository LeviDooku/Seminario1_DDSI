# schema

"""
Crea la infraestructura física de la base de datos usada por la aplicación.
(Punto 1 del seminario)

https://github.com/mkleehammer/pyodbc/wiki

Nota: se puede consultar crear_bd.sql
"""

from __future__ import annotations
import pyodbc

"""
Función drop_tables:
Elimina todas las tablas, si existen, en caso contrario, no hace nada
"""
def drop_tables(conn: pyodbc.Connection) -> None:
    drops = [
        "DROP TABLE DETALLE_PEDIDO CASCADE CONSTRAINTS",
        "DROP TABLE PEDIDO CASCADE CONSTRAINTS",
        "DROP TABLE STOCK CASCADE CONSTRAINTS",
    ]

    with conn.cursor() as cur:
        for sql in drops:
            try:
                cur.execute(sql)
            except Exception:
                pass

"""
Función create_tables:
Crea las tablas especificadas
"""
def create_tables(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cur:
        
        cur.execute("""
            CREATE TABLE STOCK(
                CPRODUCTO NUMBER(10)    PRIMARY KEY,
                CANTIDAD  NUMBER(10)    NOT NULL CHECK (CANTIDAD >= 0)
            )           
        """)

        cur.execute("""
            CREATE TABLE PEDIDO(
                CPEDIDO       NUMBER(10) PRIMARY KEY,
                CCLIENTE      NUMBER(10) NOT NULL,
                FECHA_PEDIDO  DATE       NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE DETALLE_PEDIDO(
                CPEDIDO    NUMBER(10) NOT NULL,
                CPRODUCTO  NUMBER(10) NOT NULL,
                CANTIDAD   NUMBER(10) NOT NULL CHECK (CANTIDAD > 0),
                CONSTRAINT PK_DETALLE_PEDIDO PRIMARY KEY (CPEDIDO, CPRODUCTO),
                CONSTRAINT FK_DP_PEDIDO FOREIGN KEY (CPEDIDO)   REFERENCES PEDIDO(CPEDIDO)   ON DELETE CASCADE,
                CONSTRAINT FK_DP_STOCK  FOREIGN KEY (CPRODUCTO) REFERENCES STOCK(CPRODUCTO)
            )            
        """)

"""
Función insert_stock:
Inserta las 10 tuplas (números random) en Stock
"""
def insert_stock(conn: pyodbc.Connection) -> None:
    productos = [
        (1, 50),
        (2, 28),
        (3, 4),
        (4, 21),
        (5, 6),
        (6, 67),
        (7, 92),
        (8, 100),
        (9, 23),
        (10, 34),
    ]

    with conn.cursor() as cur: 
        for cprod, cant in productos:
            cur.execute(
                "INSERT INTO STOCK (CPRODUCTO, CANTIDAD) VALUES (?, ?)",
                (cprod, cant)
            )

""""
Función resetea:
Resetea el esquema a la configuración inicial
"""
def resetea(conn: pyodbc.Connection) -> None:
    drop_tables(conn)
    create_tables(conn)
    insert_stock(conn)
    conn.commit()


