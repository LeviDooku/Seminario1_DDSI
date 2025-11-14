# GUI

import tkinter as tk
from tkinter import ttk
import sys
import io

from schema import resetea          # opción 1 del menú
from mostrar import mostrar_todo    # opción 3 del menú
from pedidos_service import iniciar_pedido, PedidoYaExisteError, anadir_detalle, SinStockError, ProductoNoExisteError, PedidoError, eliminar_detalles_pedido, cancelar_pedido, finalizar_pedido # opción 2 del menú

# ---------- boton de finalizar pedido ----------

def boton_finalizar_pedido(ventana_menu_pedido, ventana_alta, conn, cpedido):
    try:
        # Commit de todos los cambios
        finalizar_pedido(conn)  # función de pedidos_service que hace conn.commit()

        # Mensaje de éxito
        ventana_msg = tk.Toplevel()
        ventana_msg.title("Pedido finalizado")
        ventana_msg.geometry("400x150")
        ventana_msg.config(bg="#f0f0f0")

        tk.Label(
            ventana_msg,
            text=f"El pedido {cpedido} ha sido finalizado correctamente.",
            font=("Arial", 12),
            wraplength=350,
            justify="center",
            bg="#f0f0f0"
        ).pack(pady=20)

        tk.Button(
            ventana_msg,
            text="Cerrar",
            font=("Arial", 12, "bold"),
            bg="#5cb85c",
            fg="white",
            command=ventana_msg.destroy
        ).pack(pady=10)

        # Cerrar ventanas intermedias
        ventana_menu_pedido.destroy()
        ventana_alta.destroy()

    except Exception as e:
        mostrar_error_gui(ventana_menu_pedido, f"No se pudo finalizar el pedido:\n{e}")


# ---------- boton de cancelar el pedido --------

def boton_cancelar_pedido(ventana_pedido, ventana_alta, conn, cpedido):
    try:
        # Borrar pedido y detalles
        cancelar_pedido(conn)

        # Mostrar mensaje de éxito
        ventana_msg = tk.Toplevel()
        ventana_msg.title("Pedido cancelado")
        ventana_msg.geometry("400x150")
        ventana_msg.config(bg="#f0f0f0")

        tk.Label(
            ventana_msg,
            text=f"El pedido {cpedido} ha sido cancelado correctamente.",
            font=("Arial", 12),
            wraplength=350,
            justify="center",
            bg="#f0f0f0"
        ).pack(pady=20)

        tk.Button(
            ventana_msg,
            text="Cerrar",
            font=("Arial", 12, "bold"),
            bg="#5cb85c",
            fg="white",
            command=ventana_msg.destroy
        ).pack(pady=10)

        # Cerrar ventana del pedido y volver al menú principal
        ventana_pedido.destroy()
        ventana_alta.destroy()

    except Exception as e:
        mostrar_error_gui(ventana_pedido, f"No se pudo cancelar el pedido:\n{e}")


# ---------- boton de eliminar todos los detalles del producto ----------

def eliminar_detalles_gui(ventana_padre, conn, cpedido):
    try:
        eliminar_detalles_pedido(conn, cpedido)

        # Mostrar mensaje de éxito
        ventana_msg = tk.Toplevel(ventana_padre)
        ventana_msg.title("Éxito")
        ventana_msg.geometry("400x150")
        ventana_msg.config(bg="#f0f0f0")

        tk.Label(
            ventana_msg,
            text="Todos los detalles del pedido han sido eliminados correctamente.",
            font=("Arial", 12),
            wraplength=350,
            justify="center",
            bg="#f0f0f0"
        ).pack(pady=20)

        tk.Button(
            ventana_msg,
            text="Cerrar",
            font=("Arial", 12, "bold"),
            bg="#5cb85c",
            fg="white",
            command=ventana_msg.destroy
        ).pack(pady=10)

        # Después de la opción 2: mostrar contenido de la BD
        boton_mostrar_tablas(conn)

    except Exception as e:
        mostrar_error_gui(ventana_padre, str(e))


# ---------- boton de añadir detalle de producto ----------

def boton_anadir_detalles_pedido(ventana_padre, conn, cpedido):
    ventana_detalle = tk.Toplevel(ventana_padre)
    ventana_detalle.title("Añadir detalle")
    ventana_detalle.geometry("400x250")
    ventana_detalle.config(bg="#f0f0f0")

    tk.Label(ventana_detalle, text="Código producto:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_prod = tk.Entry(ventana_detalle, font=("Arial", 12))
    entry_prod.pack(pady=5)

    tk.Label(ventana_detalle, text="Cantidad:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    entry_cant = tk.Entry(ventana_detalle, font=("Arial", 12))
    entry_cant.pack(pady=5)

    def insertar_detalle():
        try:
            cproducto = int(entry_prod.get())
            cantidad = int(entry_cant.get())
            anadir_detalle(conn, cpedido, cproducto, cantidad)

            # Mensaje de éxito
            ok = tk.Toplevel(ventana_detalle)
            ok.title("Éxito")
            tk.Label(ok, text="Detalle insertado correctamente.", font=("Arial", 12)).pack(pady=15)
            tk.Button(ok, text="Cerrar", command=ok.destroy).pack(pady=10)

            ventana_detalle.destroy()

        except Exception as e:
            mostrar_error_gui(ventana_detalle, str(e))

    tk.Button(
        ventana_detalle,
        text="Insertar detalle",
        font=("Arial", 12, "bold"),
        bg="#5cb85c",
        fg="white",
        command=insertar_detalle
    ).pack(pady=15)

    tk.Button(
        ventana_detalle,
        text="Cancelar",
        font=("Arial", 12),
        bg="#d9534f",
        fg="white",
        command=ventana_detalle.destroy
    ).pack(pady=5)


# ---------- Ventana 3: menú de acciones del pedido ----------
def mostrar_menu_pedido(ventana_padre, conn, cpedido):
    ventana_pedido = tk.Toplevel(ventana_padre)
    ventana_pedido.title("Gestión del pedido")
    ventana_pedido.geometry("800x500")  # Ventana más grande
    ventana_pedido.config(bg="#f0f0f0")

    titulo = tk.Label(
        ventana_pedido,
        text="Opciones del pedido",
        font=("Arial", 22, "bold"),
        bg="#f0f0f0"
    )
    titulo.pack(pady=30)

    # Frame para cuadrícula de botones
    frame_botones = tk.Frame(ventana_pedido, bg="#f0f0f0")
    frame_botones.pack(pady=20)

    opciones = [
        ("Añadir detalle de producto",lambda: boton_anadir_detalles_pedido(ventana_pedido, conn, cpedido)), 
        ("Eliminar todos los detalles del producto", lambda: eliminar_detalles_gui(ventana_pedido, conn, cpedido)),
        ("Cancelar pedido", lambda: boton_cancelar_pedido(ventana_pedido, ventana_padre, conn, cpedido)),
        ("Finalizar pedido", lambda: boton_finalizar_pedido(ventana_pedido, ventana_padre, conn, cpedido))
    ]

    # De momento los botones no tienen lógica de BD.
    # Más adelante los conectaremos con pedidos_service.py
    for i, (texto, comando) in enumerate(opciones):
        boton = tk.Button(
            frame_botones,
            text=texto,
            font=("Arial", 15),
            wraplength=250,
            justify="center",
            width=25,
            height=4,
            bg="#e0e0e0",
            cursor="hand2",
            command=comando if comando is not None else lambda: None
        )
        boton.grid(row=i // 2, column=i % 2, padx=40, pady=25)

    # Botón de salida
    boton_salir = tk.Button(
        ventana_pedido,
        text="Cerrar",
        font=("Arial", 13, "bold"),
        bg="#d9534f",
        fg="white",
        cursor="hand2",
        command=ventana_pedido.destroy
    )
    boton_salir.pack(pady=20, side="bottom")

# ---------- Botón de insertar datos en pedido y función para mostrar el error aparte ----------

def boton_insertar_pedido_externo(conn, ventana, cpedido, ccliente, fecha_str):

    try:
        # Intentar crear el pedido
        iniciar_pedido(conn, cpedido, ccliente, fecha_str)
        # Guardamos el código del pedido como atributo de la ventana
        ventana.cpedido = cpedido
        # Mostrar menú de gestión del pedido
        mostrar_menu_pedido(ventana, conn, cpedido)

    except PedidoYaExisteError as e:
        mostrar_error_gui(ventana, str(e))

    except Exception as e:
        mostrar_error_gui(ventana, f"No se pudo crear el pedido:\n{e}")

def mostrar_error_gui(ventana_padre, mensaje):
    # Crea una ventana nueva para mostrar el error
    ventana_error = tk.Toplevel(ventana_padre)
    ventana_error.title("Error")
    ventana_error.geometry("500x200")
    ventana_error.config(bg="#f8d7da")

    label = tk.Label(
        ventana_error,
        text="Se produjo un error:",
        font=("Arial", 14, "bold"),
        bg="#f8d7da",
        fg="#721c24"
    )
    label.pack(pady=10)

    text = tk.Text(
        ventana_error,
        font=("Arial", 12),
        height=5,
        width=50,
        wrap="word",
        bg="#f5c6cb",
        fg="#721c24"
    )
    text.pack(padx=10, pady=10)
    text.insert("1.0", mensaje)
    text.config(state="disabled")  # Hacer que el texto no sea editable

    boton_cerrar = tk.Button(
        ventana_error,
        text="Cerrar",
        font=("Arial", 12, "bold"),
        bg="#d9534f",
        fg="white",
        cursor="hand2",
        command=ventana_error.destroy
    )
    boton_cerrar.pack(pady=10)



# ---------- Ventana 2: formulario de alta de pedido ----------
def mostrar_formulario_alta(ventana_padre, conn):
    ventana_alta = tk.Toplevel(ventana_padre)
    ventana_alta.title("Dar de alta nuevo pedido")
    ventana_alta.geometry("600x350")
    ventana_alta.config(bg="#f0f0f0")

    titulo = tk.Label(
        ventana_alta,
        text="Alta de nuevo pedido",
        font=("Arial", 20, "bold"),
        bg="#f0f0f0"
    )
    titulo.pack(pady=20)

    frame_form = tk.Frame(ventana_alta, bg="#f0f0f0")
    frame_form.pack(pady=10)

    campos = ["Código pedido", "Código cliente", "Fecha pedido"]
    entradas = {}

    for i, campo in enumerate(campos):
        label = tk.Label(frame_form, text=campo + ":", font=("Arial", 13), bg="#f0f0f0")
        label.grid(row=i, column=0, padx=10, pady=10, sticky="e")
        entrada = tk.Entry(frame_form, font=("Arial", 13), width=25)
        entrada.grid(row=i, column=1, padx=10, pady=10)
        entradas[campo] = entrada

    # Botón insertar:
    boton_insertar = tk.Button(
        frame_form,
        text="Insertar",
        font=("Arial", 13, "bold"),
        bg="#5cb85c",
        fg="white",
        cursor="hand2",
        command=lambda: boton_insertar_pedido_externo(
            conn,
            ventana_alta,
            int(entradas["Código pedido"].get()),
            int(entradas["Código cliente"].get()),
            entradas["Fecha pedido"].get().strip() or None
        )
    )
    boton_insertar.grid(row=1, column=2, padx=30, pady=10)

    boton_salir = tk.Button(
        ventana_alta,
        text="Cerrar",
        font=("Arial", 12, "bold"),
        bg="#d9534f",
        fg="white",
        cursor="hand2",
        command=ventana_alta.destroy
    )
    boton_salir.pack(pady=20, side="bottom")


# ---------- Botón de borrado y creación de nuevas tablas ----------

def boton_borrado_y_creacion_tablas(conn):
    # Ejecuta resetea
    resetea(conn)

    # Ventana de mensajes
    ventana_msg = tk.Toplevel()
    ventana_msg.title("Progreso")
    ventana_msg.geometry("400x200")
    ventana_msg.config(bg="#f0f0f0")

    cuadro_texto = tk.Text(ventana_msg, font=("Arial", 12), width=45, height=5)
    cuadro_texto.pack(padx=20, pady=20)
    cuadro_texto.insert(tk.END, "Tablas borradas exitosamente\n")
    cuadro_texto.update()

    # Mostrar mensaje tras 3 segundos
    def mostrar_segundo_mensaje():
        cuadro_texto.insert(tk.END, "Creación de nueva tabla STOCK completada\n")
        cuadro_texto.update()

    ventana_msg.after(1000, mostrar_segundo_mensaje)
    
# ---------- Botón de mostrar tablas ----------

def boton_mostrar_tablas(conn):
    ventana_tablas = tk.Toplevel()
    ventana_tablas.title("Contenido de las tablas")
    ventana_tablas.geometry("600x400")
    ventana_tablas.config(bg="#f0f0f0")

    cuadro_texto = tk.Text(ventana_tablas, font=("Arial", 12), width=70, height=20)
    cuadro_texto.pack(padx=20, pady=20)

    # Redirigir la salida de mostrar_todo al cuadro de texto
    buffer = io.StringIO()
    sys.stdout = buffer
    mostrar_todo(conn)
    sys.stdout = sys.__stdout__

    cuadro_texto.insert(tk.END, buffer.getvalue())


# ---------- Ventana 1: menú principal ----------
def iniciar_gui(conn):
    ventana = tk.Tk()
    ventana.title("Menú principal")
    ventana.geometry("900x500")
    ventana.config(bg="#f0f0f0")

    for i in range(3):
        ventana.columnconfigure(i, weight=1, minsize=250)
    for i in range(3):
        ventana.rowconfigure(i, weight=1)

    titulo = tk.Label(
        ventana,
        text="Menú principal",
        font=("Arial", 24, "bold"),
        bg="#f0f0f0"
    )
    titulo.grid(row=0, column=0, columnspan=3, pady=(40, 30))

    botones = [
        # Opción 1: Borrado y creación de nuevas tablas
        ("Borrado y creación de nuevas tablas", lambda: boton_borrado_y_creacion_tablas(conn)),

        # Opción 2: Dar de alta nuevo pedido (abre formulario)
        ("Dar de alta nuevo pedido", lambda: mostrar_formulario_alta(ventana, conn)),

        # Opción 3: Mostrar tablas
        ("Mostrar tablas", lambda: boton_mostrar_tablas(conn)),
    ]

    for i, (texto, comando) in enumerate(botones):
        boton = tk.Button(
            ventana,
            text=texto,
            font=("Arial", 14),
            wraplength=220,
            justify="center",
            width=25,
            height=3,
            bg="#e0e0e0",
            relief="raised",
            cursor="hand2",
            command=comando
        )
        boton.grid(row=1, column=i, padx=25, pady=10, sticky="n")

    boton_salir = tk.Button(
        ventana,
        text="Salir",
        font=("Arial", 12, "bold"),
        width=12,
        height=2,
        bg="#d9534f",
        fg="white",
        cursor="hand2",
        command=ventana.destroy
    )
    boton_salir.grid(row=2, column=2, sticky="se", padx=40, pady=40)

    ventana.mainloop()