from tkinter import *
import tkinter as tk
from tkinter import filedialog
import json

import tkinter as tk
from tkinter import filedialog
import json

class Lexema:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

class Error:
    def __init__(self, mensaje):
        self.mensaje = mensaje

def analizadorLexico(textAreaInicial, textAreaFinal):
    pass  # Esta función no se utiliza en la implementación del proyecto

def traducir(textAreaInicial, textAreaFinal):
    contenido = textAreaInicial.get('1.0', tk.END)
    traduccion = ""
    errores = []

    try:
        datos_json = json.loads(contenido)
        if "Inicio" in datos_json:
            inicio = datos_json["Inicio"]
            if "Encabezado" in inicio and "Cuerpo" in inicio:
                encabezado = inicio["Encabezado"]
                cuerpo = inicio["Cuerpo"]
                traduccion += f"<!DOCTYPE html>\n<html>\n<head>\n<title>{encabezado['TituloPagina']}</title>\n</head>\n<body>\n"
                traduccion += traducir_cuerpo(cuerpo)
                traduccion += "</body>\n</html>"
            else:
                errores.append(Error("Falta el bloque 'Encabezado' o 'Cuerpo' en el bloque 'Inicio'"))
        else:
            errores.append(Error("Falta el bloque 'Inicio' en el archivo JSON"))

    except json.JSONDecodeError as e:
        errores.append(Error(f"Error al decodificar JSON: {e}"))

    if traduccion:
        textAreaFinal.delete('1.0', tk.END)
        textAreaFinal.insert(tk.END, traduccion)
    else:
        imprimirErrores(errores, textAreaFinal)

def traducir_cuerpo(cuerpo):
    traduccion = ""
    for elemento in cuerpo:
        for tipo, contenido in elemento.items():
            if tipo == "Titulo":
                traduccion += traducir_titulo(contenido)
            elif tipo == "Fondo":
                traduccion += traducir_fondo(contenido)
            elif tipo == "Parrafo":
                traduccion += traducir_parrafo(contenido)
            elif tipo == "Texto":
                traduccion += traducir_texto(contenido)
            elif tipo == "Codigo":
                traduccion += traducir_codigo(contenido)
            elif tipo == "Negrita":
                traduccion += traducir_negrita(contenido)
            elif tipo == "Subrayado":
                traduccion += traducir_subrayado(contenido)
            elif tipo == "Tachado":
                traduccion += traducir_tachado(contenido)
            elif tipo == "Cursiva":
                traduccion += traducir_cursiva(contenido)
            elif tipo == "Salto":
                traduccion += traducir_salto(contenido)
            elif tipo == "Tabla":
                traduccion += traducir_tabla(contenido)
            else:
                pass  # Manejo de otros tipos de elementos si es necesario
    return traduccion

def traducir_titulo(contenido):
    texto = contenido.get('texto', '')
    posicion = contenido.get('posicion', 'izquierda')
    tamaño = contenido.get('tamaño', '16')
    color = contenido.get('color', 'negro')
    return f"<h1 style=\"text-align: {posicion}; font-size: {tamaño}px; color: {color};\">{texto}</h1>\n"

def traducir_fondo(contenido):
    color = contenido.get('color', 'blanco')
    return f"<body style=\"background-color: {color};\">\n"

def traducir_parrafo(contenido):
    texto = contenido.get('texto', '')
    posicion = contenido.get('posicion', 'izquierda')
    return f"<p style=\"text-align: {posicion};\">{texto}</p>\n"

def traducir_texto(contenido):
    texto = contenido.get('texto', '')
    estilo = f"font-family: {contenido.get('fuente', 'Arial')}; color: {contenido.get('color', 'negro')}; font-size: {contenido.get('tamaño', '12')}px;"
    if "tachado" in contenido:
        estilo += " text-decoration: line-through;"
    if "subrayado" in contenido:
        estilo += " text-decoration: underline;"
    if "cursiva" in contenido:
        estilo += " font-style: italic;"
    return f"<span style=\"{estilo}\">{texto}</span>\n"

def traducir_codigo(contenido):
    texto = contenido.get('texto', '')
    posicion = contenido.get('posicion', 'izquierda')
    return f"<code style=\"text-align: {posicion};\">{texto}</code>\n"

def traducir_negrita(contenido):
    texto = contenido.get('texto', '')
    return f"<b>{texto}</b>\n"

def traducir_subrayado(contenido):
    texto = contenido.get('texto', '')
    return f"<u>{texto}</u>\n"

def traducir_tachado(contenido):
    texto = contenido.get('texto', '')
    return f"<s>{texto}</s>\n"

def traducir_cursiva(contenido):
    texto = contenido.get('texto', '')
    return f"<i>{texto}</i>\n"

def traducir_salto(contenido):
    cantidad = contenido.get('cantidad', '1')
    return f"<br>\n" * int(cantidad)

def traducir_tabla(contenido):
    filas = contenido.get('filas', '0')
    columnas = contenido.get('columnas', '0')
    tabla_html = f"<table border='1'>\n"
    for i in range(int(filas)):
        tabla_html += "<tr>\n"
        for j in range(int(columnas)):
            elemento = contenido.get('elemento', {}).get(f"{i+1}-{j+1}", '')
            tabla_html += f"<td>{elemento}</td>\n"
        tabla_html += "</tr>\n"
    tabla_html += "</table>\n"
    return tabla_html

def imprimirErrores(errores, textAreaFinal):
    textAreaFinal.delete("1.0", tk.END)
    textAreaFinal.insert(tk.END, "Errores encontrados:\n")
    for error in errores:
        textAreaFinal.insert(tk.END, f"{error.mensaje}\n")

def abrir_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivo JSON", "*.json")])
    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()
        textAreaInicial.delete("1.0", tk.END)
        textAreaInicial.insert(tk.END, contenido)

def salir():
    ventana.quit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Traductor HTML")
ventana.configure(bg="#BFEA7C")  # Establecer color de fondo

# Ampliar el tamaño de la ventana
ventana.geometry("1000x600")

# Crear un contenedor Frame para los botones
frame_botones = tk.Frame(ventana, bg="#BFEA7C")
frame_botones.pack(pady=20)

# Crear los botones
boton_abrir = tk.Button(frame_botones, text="Abrir archivo", command=abrir_archivo, width=15)
boton_abrir.pack(side=tk.LEFT, padx=10)

boton_traducir = tk.Button(frame_botones, text="Traducir", command=lambda: traducir(textAreaInicial, textAreaFinal), width=15)
boton_traducir.pack(side=tk.LEFT, padx=10)

boton_salir = tk.Button(frame_botones, text="Salir", command=salir, width=15)
boton_salir.pack(side=tk.LEFT, padx=10)

# Crear un contenedor Frame para los TextAreas
frame_textareas = tk.Frame(ventana, bg="#BFEA7C")
frame_textareas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Crear el primer textarea
textAreaInicial = tk.Text(frame_textareas, height=20, width=40)
textAreaInicial.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Crear el segundo textarea
textAreaFinal = tk.Text(frame_textareas, height=20, width=40)
textAreaFinal.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Ejecutar el bucle principal
ventana.mainloop()
