# pedidos_service

"""
Gestiona la lógica de pedidos del menú "Dar de alta a nuevo pedido"
(Punto 2 del seminario)
"""

from __future__ import annotations
from typing import Optional
import pyodbc

SAVEPOINT_NAME = "sp_pedido_creado"


#Excepciones específicas

class PedidoError(RuntimeError):
    """Error genérico relacionado con la gestión de pedidos."""
    pass


class PedidoYaExisteError(PedidoError):
    """Se intenta crear un pedido con un código que ya existe."""
    pass


class ProductoNoExisteError(PedidoError):
    """El código de producto no existe en la tabla Stock."""
    pass


class SinStockError(PedidoError):
    """No hay suficiente stock para el producto solicitado."""
    pass


#Funciones 

"""
Función iniciar_pedido:
Inserta en Pedido, crea un savepoint para poder deshacer los detalles. No hace commit
"""
def iniciar_pedido(conn: pyodbc.Connection, cpedido: int, ccliente: int, fecha_str: Optional[str] = None) -> int:
    with conn.cursor() as cur:
        # Comprobar que no exista ya ese Cpedido
        cur.execute("SELECT COUNT(*) FROM PEDIDO WHERE CPEDIDO = ?", (cpedido,))
        (n,) = cur.fetchone()
        if n > 0:
            raise PedidoYaExisteError(
                f"Ya existe un pedido con código {cpedido}."
            )

        #INSERT del pedido
        if fecha_str:
            #Si se proporciona fecha, la usamos explícitamente
            cur.execute(
                """
                INSERT INTO PEDIDO (CPEDIDO, CCLIENTE, FECHA_PEDIDO)
                VALUES (?, ?, TO_DATE(?, 'YYYY-MM-DD HH24:MI:SS'))
                """,
                (cpedido, ccliente, fecha_str),
            )
        else:
            #Usar sysdate siempre que no se pase fecha
            cur.execute(
                """
                INSERT INTO PEDIDO (CPEDIDO, CCLIENTE, FECHA_PEDIDO)
                VALUES (?, ?, SYSDATE)
                """,
                (cpedido, ccliente),
            )

    #Savepoint sobre la conexión
    conn.execute(f"SAVEPOINT {SAVEPOINT_NAME}")

    return cpedido


"""
Función añadir_detalle:
Añade un detalle al pedido.
Primero comprueba que existe, comprueba el producto y su stock
Inserta en Detalle_Pedido y acutaliza Stock, restando la cantidad

No hace commit ni rollback
"""
def anadir_detalle(conn: pyodbc.Connection, cpedido: int, cproducto: int,cantidad: int) -> None:
    if cantidad <= 0:
        raise PedidoError("La cantidad debe ser mayor que 0.")

    with conn.cursor() as cur:
        #Comprobar que existe el pedido
        cur.execute("SELECT 1 FROM PEDIDO WHERE CPEDIDO = ?", (cpedido,))
        if cur.fetchone() is None:
            raise PedidoError(
                f"No existe el pedido {cpedido}. ¿Se ha iniciado correctamente?"
            )

        #Comprobar que existe el producto y ver su stock
        cur.execute(
            "SELECT CANTIDAD FROM STOCK WHERE CPRODUCTO = ?",
            (cproducto,),
        )
        row = cur.fetchone()
        if row is None:
            raise ProductoNoExisteError(
                f"El producto {cproducto} no existe en Stock."
            )

        stock_disponible = row[0]
        if cantidad > stock_disponible:
            raise SinStockError(
                f"Stock insuficiente para el producto {cproducto}: "
                f"disponible {stock_disponible}, solicitado {cantidad}."
            )

        #Insertar detalle de pedido
        cur.execute(
            """
            INSERT INTO Detalle_Pedido (Cpedido, Cproducto, Cantidad)
            VALUES (?, ?, ?)
            """,
            (cpedido, cproducto, cantidad),
        )

        #Actualizar stock
        cur.execute(
            """
            UPDATE Stock
            SET Cantidad = Cantidad - ?
            WHERE Cproducto = ?
            """,
            (cantidad, cproducto),
        )

"""
Función eliminar_detalles_pedido:
Hace rollback sp_pedido_creado, deshace detalles y cambios en el Stock, pero mantiene el pedido en si
Vuelve a crear el savepoint para seguir trabajando
No hace commit
"""
def eliminar_detalles_pedido(conn: pyodbc.Connection) -> None:
    with conn.cursor() as cur:
        try:
            #Deshacer todo lo ocurrido después de crear el pedido
            conn.execute(f"ROLLBACK TO {SAVEPOINT_NAME}")
        except pyodbc.Error as e:
            raise PedidoError(
                "No se ha podido hacer ROLLBACK TO SAVEPOINT. "
                "¿Se ha iniciado ya el pedido?"
            ) from e

        #Crear de nuevo el savepoint en el estado "solo pedido"
        conn.execute(f"SAVEPOINT {SAVEPOINT_NAME}")

"""
Función cancelar_pedido:
Cancela completamente el pedido actual
Hace  rollback total de la transacción
"""
def cancelar_pedido(conn: pyodbc.Connection) -> None:
    conn.rollback()

"""
Función finalizar_pedido:
Finaliza el pedido actual, esto es, hace commit de la transacción
"""
def finalizar_pedido(conn: pyodbc.Connection) -> None:
    conn.commit()
