import os
import sqlite3
import random
import ttkbootstrap as ttk
import pyperclip
from tkinter import messagebox

# ------------------------
# Funciones de Base de Datos y Lógica
# ------------------------

def guardar_contrasena_en_db(contrasena, pagina, correo):
    conn = sqlite3.connect('contrasenas.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS contrasenas (id INTEGER PRIMARY KEY, contrasena TEXT, pagina TEXT, correo TEXT)'
    )
    cursor.execute(
        'INSERT INTO contrasenas (contrasena, pagina, correo) VALUES (?, ?, ?)',
        (contrasena, pagina, correo)
    )
    conn.commit()
    conn.close()

def generar_contrasena(longitud=12):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*_+"
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def generar_y_mostrar():
    try:
        longitud = int(entry_longitud.get())
        contrasena = generar_contrasena(longitud)
        label_contrasena.config(text=contrasena)
    except ValueError:
        label_contrasena.config(text="Por favor ingresa un número válido")

def copiar_contrasena():
    contrasena = label_contrasena.cget("text")
    if contrasena:
        pyperclip.copy(contrasena)
        messagebox.showinfo("Éxito", "Contraseña copiada al portapapeles!")
    else:
        messagebox.showerror("Error", "No hay contraseña para copiar")

def guardar_todo():
    if combo_opciones.get() == "Generar una contraseña":
        contrasena = label_contrasena.cget("text")
        pagina = entry_pagina.get()
        correo = entry_correo.get()
        if '@' not in correo:
            messagebox.showerror("Error", "El correo debe contener '@'")
            return
    else:
        contrasena = entry_contrasena_personalizada.get()
        pagina = entry_pagina.get()
        correo = entry_correo.get()
        if '@' not in correo:
            messagebox.showerror("Error", "El correo debe contener '@'")
            return
    if pagina and correo and contrasena:
        guardar_contrasena_en_db(contrasena, pagina, correo)
        messagebox.showinfo("Éxito", "¡Datos guardados con éxito!")
    else:
        messagebox.showerror("Error", "Por favor completa todos los campos.")

# ------------------------
# Función para mostrar u ocultar widgets según opción seleccionada
# ------------------------

def mostrar_opciones_seleccionadas(event):
    if combo_opciones.get() == "Generar una contraseña":
        label_pagina.pack(pady=5)
        entry_pagina.pack(pady=5)
        label_correo.pack(pady=5)
        entry_correo.pack(pady=5)
        label_longitud.pack(pady=5)
        entry_longitud.pack(pady=5)
        boton_generar.pack(pady=5)
        label_contrasena.pack(pady=5)
        boton_copiar.pack(pady=5)
        label_contrasena_personalizada.pack_forget()
        entry_contrasena_personalizada.pack_forget()
        boton_guardar.pack(pady=5)
    elif combo_opciones.get() == "Escribir una contraseña propia":
        label_pagina.pack(pady=5)
        entry_pagina.pack(pady=5)
        label_correo.pack(pady=5)
        entry_correo.pack(pady=5)
        label_contrasena_personalizada.pack(pady=5)
        entry_contrasena_personalizada.pack(pady=5)
        boton_guardar.pack(pady=5)
        label_longitud.pack_forget()
        entry_longitud.pack_forget()
        boton_generar.pack_forget()
        label_contrasena.pack_forget()
        boton_copiar.pack_forget()

# ------------------------
# Configuración de la Ventana Principal
# ------------------------

root = ttk.Window(themename='darkly')
root.title("Gestión de Contraseñas")
root.geometry("500x750")

icono_path = os.path.abspath("C:/Users/Usuario19/Documents/Deipro/python/girasol_i2o_icon.ico")
if os.path.exists(icono_path):
    root.iconbitmap(icono_path)
else:
    print(f"Advertencia: No se encontró el icono en {icono_path}")

frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

root.style.configure("TLabel", font=("Consolas", 14), foreground="white")
root.style.configure("TButton", font=("Consolas", 14), padding=10)
root.style.configure("TEntry", font=("Consolas", 14))

# ------------------------
# Widgets Comunes
# ------------------------

label_opciones = ttk.Label(frame, text="Selecciona una opción:", style="TLabel")
label_opciones.pack(pady=10)

combo_opciones = ttk.Combobox(
    frame,
    values=["Generar una contraseña", "Escribir una contraseña propia"],
    font=("Consolas", 14),
    width=30  # Ajuste de la anchura de la caja
)
combo_opciones.bind("<<ComboboxSelected>>", mostrar_opciones_seleccionadas)
combo_opciones.pack(pady=10)

label_pagina = ttk.Label(frame, text="Página Relacionada:", style="TLabel")
entry_pagina = ttk.Entry(frame, font=("Consolas", 14), width=30)
label_correo = ttk.Label(frame, text="Correo Relacionado:", style="TLabel")
entry_correo = ttk.Entry(frame, font=("Consolas", 14), width=30)

# Widgets para el modo "Generar una contraseña":
label_longitud = ttk.Label(frame, text="Longitud de la contraseña:", style="TLabel")
entry_longitud = ttk.Entry(frame, font=("Consolas", 14), width=10)
boton_generar = ttk.Button(frame, text="Generar Contraseña", command=generar_y_mostrar, style="TButton")
label_contrasena = ttk.Label(frame, text="", style="TLabel")
boton_copiar = ttk.Button(frame, text="Copiar Contraseña", command=copiar_contrasena, style="TButton")

# Widgets para el modo "Escribir una contraseña propia":
label_contrasena_personalizada = ttk.Label(frame, text="Escribe tu propia Contraseña:", style="TLabel")
entry_contrasena_personalizada = ttk.Entry(frame, font=("Consolas", 14), show="*", width=30)

# Botón de guardar (común a ambos modos)
boton_guardar = ttk.Button(frame, text="Guardar Todo", command=guardar_todo, style="TButton")

root.mainloop()
