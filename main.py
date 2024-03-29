import tkinter as tk
from tkinter import filedialog
from analizadorLexico import analizadorLexico, analizar_texto, imprimirLexemasYErrores
from traductor_html import traducir_a_html
from lexema import Lexema, Error

def abrir_archivo():
    archivo = filedialog.askopenfilename()
    if archivo:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        textAreaInicial.delete("1.0", tk.END)
        textAreaInicial.insert(tk.END, contenido)


def analizar_texto_y_mostrar_html():
    texto = textAreaInicial.get("1.0", tk.END)
    tokens_encontrados = analizar_texto(texto)
    lexemas, errores = analizadorLexico(textAreaInicial, textAreaFinal)
    imprimirLexemasYErrores(lexemas, errores)
    html_generado = traducir_a_html(tokens_encontrados)
    textAreaFinal.delete("1.0", tk.END)
    textAreaFinal.insert(tk.END, html_generado)
    textAreaFinal.config(state="disabled")

def salir():
    ventana.quit()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Traductor HTML")
ventana.configure(bg="#BFEA7C") 
ventana.geometry("1000x600")

# Contenedor para los botones
frame_botones = tk.Frame(ventana, bg="#BFEA7C")
frame_botones.pack(pady=20)

# Botones
boton_abrir = tk.Button(frame_botones, text="Abrir archivo", command=abrir_archivo, width=15)
boton_abrir.pack(side=tk.LEFT, padx=10)

boton_traducir = tk.Button(frame_botones, text="Traducir a HTML", command=analizar_texto_y_mostrar_html, width=15)
boton_traducir.pack(side=tk.LEFT, padx=10)

boton_salir = tk.Button(frame_botones, text="Salir", command=salir, width=15)
boton_salir.pack(side=tk.LEFT, padx=10)

# Contenedor para los TextAreas
frame_textareas = tk.Frame(ventana, bg="#BFEA7C")
frame_textareas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Primer textarea
textAreaInicial = tk.Text(frame_textareas, height=20, width=40)
textAreaInicial.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

# Segundo textarea
textAreaFinal = tk.Text(frame_textareas, height=20, width=40, state="normal")
textAreaFinal.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

ventana.mainloop()