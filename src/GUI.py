import tkinter as tk
from tkinter import ttk


# ---------- Ventana 3: menú de acciones del pedido ----------
def mostrar_menu_pedido(ventana_padre):
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
        "Añadir detalle de producto",
        "Eliminar todos los detalles del producto",
        "Cancelar pedido",
        "Finalizar pedido"
    ]

    # Crear botones en 2x2
    for i, texto in enumerate(opciones):
        boton = tk.Button(
            frame_botones,
            text=texto,
            font=("Arial", 15),
            wraplength=250,      # Permite que el texto se divida en varias líneas
            justify="center",    # Centra el texto en el botón
            width=25,
            height=4,
            bg="#e0e0e0",
            cursor="hand2"
        )
        boton.grid(row=i // 2, column=i % 2, padx=40, pady=25)  # Más espacio entre botones

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


# ---------- Ventana 2: formulario de alta de pedido ----------
def mostrar_formulario_alta(ventana_padre):
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

    # Botón insertar
    boton_insertar = tk.Button(
        frame_form,
        text="Insertar",
        font=("Arial", 13, "bold"),
        bg="#5cb85c",
        fg="white",
        cursor="hand2",
        command=lambda: mostrar_menu_pedido(ventana_alta)
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


# ---------- Ventana 1: menú principal ----------
def iniciar_gui():
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
        ("Borrado y creación de nuevas tablas", None),
        ("Dar de alta nuevo pedido", lambda: mostrar_formulario_alta(ventana)),
        ("Mostrar tablas", None)
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
