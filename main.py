import tkinter as tk
from tkinter import filedialog
import re

class Lexema:
    def __init__(self, tipo, valor, linea=None, columna=None):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

class Error:
    def __init__(self, mensaje, fila, columna):
        self.mensaje = mensaje
        self.fila = fila
        self.columna = columna

def abrir_archivo():
    archivo = filedialog.askopenfilename()
    if archivo:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        textAreaInicial.delete("1.0", tk.END)
        textAreaInicial.insert(tk.END, contenido)

def analizadorLexico(textAreaInicial, textAreaFinal):
    lexemas = []
    errores = []
    palabra = ""
    dentro_cadena = False  
    
    # Obtener el texto del text area
    texto = textAreaInicial.get("1.0", "end")
    
    # Inicializar las variables de fila y columna
    fila = 1
    columna = 0
    
    # Iterar sobre cada caracter del texto
    for char in texto:
        columna += 1
        # Se verifica si está dentro de una cadena de texto
        if char == '"':
            dentro_cadena = not dentro_cadena
            palabra += char
            continue
        
        # Si está dentro de una cadena de texto, se añade el caracter a la palabra
        if dentro_cadena:
            palabra += char
            continue
        
        # Se verifica que el caracter sea una letra, un dígito o un carácter especial
        if char.isalnum(): 
            palabra += char
        else:
            if palabra:
                # Verificar si la palabra es una palabra reservada
                if palabra in ['Inicio', 'Encabezado', 'TituloPagina', 'Cuerpo', 'Titulo', 'texto', 'posicion', 'tamaño', 'color', 'Fondo', 'Parrafo', 'fuente', 'Texto', 'Codigo', 'Negrita', 'Subrayado', 'Tachado', 'Cursiva', 'Tabla', 'filas', 'columnas', 'elemento', 'fila', 'columna', 'Salto', 'cantidad']:
                    lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
                elif palabra.isdigit():
                    lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
                else:
                    lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
                palabra = ""
            
            # Otros caracteres especiales
            if char in [',']:
                lexemas.append(Lexema("Coma", char, fila, columna))
            elif char in ['.']:
                lexemas.append(Lexema("Punto", char, fila, columna))
            elif char in ['{']:
                lexemas.append(Lexema("Llave de apertura", char, fila, columna))
            elif char in ['}']:
                lexemas.append(Lexema("Llave de cierre", char, fila, columna))
            elif char in [':']:
                lexemas.append(Lexema("Dos puntos", char, fila, columna))
            elif char in ['[']:
                lexemas.append(Lexema("Corchete de apertura", char, fila, columna))
            elif char in [']']:
                lexemas.append(Lexema("Corchete de cierre", char, fila, columna))    
            elif char in [';']:
                lexemas.append(Lexema("Punto y coma", char, fila, columna))                            
            elif char in [' ']:
                continue
            elif char == '\n':
                fila += 1
                columna = 0  # Reiniciar la columna cuando se encuentra un salto de línea
                continue                                        
            else:
                errores.append(Error(f"{char}", fila, columna))
    
    # Verificar si hay una palabra aún por agregar
    if palabra:
        if palabra in ['Inicio', 'Encabezado', 'TituloPagina', 'Cuerpo', 'Titulo', 'texto', 'posicion', 'tamaño', 'color', 'Fondo', 'Parrafo', 'fuente', 'Texto', 'Codigo', 'Negrita', 'Subrayado', 'Tachado', 'Cursiva', 'Tabla', 'filas', 'columnas', 'elemento', 'fila', 'columna', 'Salto', 'cantidad']:
            lexemas.append(Lexema("Palabra Reservada", palabra, fila, columna - len(palabra)))
        elif palabra.isdigit():
            lexemas.append(Lexema("Número", palabra, fila, columna - len(palabra)))
        else:
            lexemas.append(Lexema("Cadena", palabra, fila, columna - len(palabra)))
    
    imprimirLexemasYErrores(lexemas, errores)


def imprimirLexemasYErrores(lexemas, errores):
    # Escribir los errores en un archivo HTML
    with open("errores.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Errores Léxicos</title>\n</head>\n<body>\n")
        f.write("<h1>Errores Léxicos</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Caracter Inválido</th><th>Cantidad</th><th>Fila</th><th>Columna</th></tr>\n")
        caracteres_invalidos = {}
        for error in errores:
            if error.mensaje not in caracteres_invalidos:
                caracteres_invalidos[error.mensaje] = {"cantidad": 1, "fila": error.fila, "columna": error.columna}
            else:
                caracteres_invalidos[error.mensaje]["cantidad"] += 1
        for caracter, info in caracteres_invalidos.items():
            f.write(f"<tr><td>{caracter}</td><td>{info['cantidad']}</td><td>{info['fila']}</td><td>{info['columna']}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n</html>")

        # Escribir los lexemas en un archivo HTML
    with open("lexemas.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Listado de Tokens y Lexemas</title>\n</head>\n<body>\n")
        f.write("<h1>Listado de Tokens y Lexemas</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Token</th><th>Lexema</th><th>Línea</th><th>Columna</th></tr>\n")
        for lexema in lexemas:
            f.write(f"<tr><td>{lexema.tipo}</td><td>{lexema.valor}</td><td>{lexema.linea}</td><td>{lexema.columna}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n</html>")

def analizar_texto(texto):
    tokens = []
    #Patrones para buscar los tokens y sus valores
    patrones = {
        'INICIO': r'Inicio:\s*{',
        'ENCABEZADO': r'Encabezado:\s*{',
        'TITULOPAGINA': r'TituloPagina:\s*\"(.*?)\";',
        'POSICION': r'posicion:\s*\"(.*?)\"',
        'TAMAÑO': r'tamaño:\s*\"(.*?)\"',
        'CUERPO': r'Cuerpo:\s*\[([^]]+)\]',
        'TITULO': r'Titulo:\s*{([^}]+)}',
        'PARRAFO': r'Parrafo:\s*{([^}]+)}',
        'FONDO': r'Fondo:\s*{([^}]+)}',
        'TEXTO': r'Texto:\s*{([^}]+)}',
        'CODIGO': r'Codigo:\s*{([^}]+)}',
        'NEGRITA': r'Negrita:\s*{([^}]+)}',
        'SUBRAYADO': r'Subrayado:\s*{([^}]+)}',
        'TACHADO': r'Tachado:\s*{([^}]+)}',
        'CURSIVA': r'Cursiva:\s*{([^}]+)}',
        'SALTO': r'Salto:\s*{cantidad:\s*\"(\d+)\"\s*};',
        'TABLA': r'Tabla:\s*{([^}]+)}'
    }
    
    # Buscar los patrones en el texto y se extraen los tokens y valores
    for token, patron in patrones.items():
        matches = re.findall(patron, texto, re.MULTILINE | re.DOTALL)
        for match in matches:
            tokens.append((token, match))
    
    print("Tokens encontrados:")
    for token in tokens:
        print(token)
    
    return tokens

def convertir_color_a_hexadecimal(color):
    colores = {
        'rojo': '#FF0000',
        'amarillo': '#FFFF00',
        'azul': '#0000FF',
        'cyan': '#00FFFF'
        # Pendiente: agregar más colores
    }
    # Pasar color a hexadecimal
    if color.lower() in colores:
        return colores[color.lower()]
    # Si es exadecimal dejarlo asi
    elif color.startswith('#') and len(color) == 7 and all(c in '0123456789ABCDEFabcdef' for c in color[1:]):
        return color
    # Si no, negro por defecto
    else:
        return '#000000' 

def traducir_a_html(tokens):
    html = "<!DOCTYPE html>\n<html>\n<head>\n<title>"
    titulo_pagina = ""
    cuerpo = ""
    fondo_estilo = "" 
    saltos = 0  

    # Tamaños de título a etiquetas HTML 
    tamanos_a_encabezados = {
        't1': 'h1',
        't2': 'h2',
        't3': 'h3',
        't4': 'h4',
        't5': 'h5',
        't6': 'h6'
    }

    for token, valor in tokens:
        print(f"Token: {token}, Valor: {valor}")  # Imprimir el token y su valor

        if token == 'TITULOPAGINA':
            titulo_pagina = valor
        elif token == 'FONDO':
            fondo_estilo = f"background-color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))};"
        elif token == 'TITULO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            # Pasar el tamaño del titulo a la etiqueta HTML 
            tamaño = extraer_valor(valor, 'tamaño', 't1')
            etiqueta_encabezado = tamanos_a_encabezados.get(tamaño, 'h1')
            cuerpo += f"<{etiqueta_encabezado} style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</{etiqueta_encabezado}>\n"
        elif token == 'PARRAFO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<p style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</p>\n"
        elif token == 'TEXTO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<span style='font-family:{extraer_valor(valor, 'fuente')}; color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; font-size:{extraer_valor(valor, 'tamaño')}px; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</span>\n"
        elif token == 'CODIGO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion  
            cuerpo += f"<code style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</code>\n"
        elif token == 'NEGRITA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<b style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</b>\n"
        elif token == 'SUBRAYADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<u style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</u>\n"
        elif token == 'TACHADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<strike style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</strike>\n"
        elif token == 'CURSIVA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<i style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</i>\n"
        elif token == 'TABLA':
            filas = int(extraer_valor(valor, 'filas', '0'))
            columnas = int(extraer_valor(valor, 'columnas', '0'))
            tabla_html = "<table border='1'>\n"
            elementos_tabla = extraerElementosTabla(valor)
            for fila in range(filas):
                tabla_html += "<tr>\n"
                for columna in range(columnas):
                    texto_elemento = ""
                    for elemento in elementos_tabla:
                        if int(elemento['fila']) == fila + 1 and int(elemento['columna']) == columna + 1:
                            texto_elemento = elemento['texto']
                            break
                    tabla_html += f"<td>{texto_elemento}</td>\n"
                tabla_html += "</tr>\n"
            tabla_html += "</table>\n"
            cuerpo += tabla_html
        elif token == 'SALTO':
            cantidad_saltos = int(extraer_valor(valor, 'cantidad', '1'))
            print(f"SALTOS DE LÍNEA: {cantidad_saltos}")  # verificar la cantidad de saltos de línea
            cuerpo += "<br>" * cantidad_saltos 
            print(f"CUERPO DESPUÉS DEL SALTO: {cuerpo}")  # verificar después de agregar los saltos de línea
    
    html += f"{titulo_pagina}</title>\n</head>\n<body style='{fondo_estilo}'>\n{cuerpo}</body>\n</html>"
    return html


def extraerElementosTabla(token_str):
    # Patron para encontrar todos los elementos de la tabla
    elemento_pattern = r'elemento:{"fila":"(\d+)","columna":"(\d+)","([^"]*)"}'
    matches = re.findall(elemento_pattern, token_str)
    elementos = []
    for match in matches:
        elemento = {
            'fila': match[0],
            'columna': match[1],
            'texto': match[2]
        }
        elementos.append(elemento)
    return elementos

def extraer_valor(token_str, atributo, valor_predeterminado=""):
    # RE para buscar el valor del atributo en la cadena del token
    patron = rf'{atributo}:\s*"([^"]*)"'
    matches = re.findall(patron, token_str)
    if matches:
        return matches[0]
    return valor_predeterminado if atributo != "posicion" else "left"


def analizar_texto_y_mostrar_html():
    texto = textAreaInicial.get("1.0", tk.END)
    tokens_encontrados = analizar_texto(texto)
    analizadorLexico(textAreaInicial, textAreaFinal)  
    html_generado = traducir_a_html(tokens_encontrados)
    textAreaFinal.delete("1.0", tk.END)
    textAreaFinal.insert(tk.END, html_generado)

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
textAreaFinal = tk.Text(frame_textareas, height=20, width=40)
textAreaFinal.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

ventana.mainloop()