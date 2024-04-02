import re
from lexema import Lexema

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
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion
            # Pasar el tamaño del titulo a la etiqueta HTML
            tamaño = extraer_valor(valor, 'tamaño', 't1')
            etiqueta_encabezado = tamanos_a_encabezados.get(tamaño, 'h1')
            cuerpo += f"<{etiqueta_encabezado} style='color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</{etiqueta_encabezado}>\n"
        elif token == 'PARRAFO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion
            cuerpo += f"<p style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</p>\n"
        elif token == 'TEXTO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion
            cuerpo += f"<span style='font-family:{extraer_valor(valor, 'fuente', 'Arial')}; font-size:{extraer_valor(valor, 'tamaño', '12')}px; color:{convertir_color_a_hexadecimal(extraer_valor(valor, 'color', 'black'))}; text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</span>\n"
        elif token == 'CODIGO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            alineacion = 'center' if alineacion == 'centro' else alineacion
            alineacion = 'right' if alineacion == 'derecha' else alineacion
            cuerpo += f"<code style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</code>\n"
        elif token == 'NEGRITA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<b style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</b>\n"
        elif token == 'SUBRAYADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<u style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</u>\n"
        elif token == 'TACHADO':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<strike style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</strike>\n"
        elif token == 'CURSIVA':
            alineacion = extraer_valor(valor, 'posicion', 'left')
            alineacion = 'left' if alineacion == 'izquierda' else alineacion
            cuerpo += f"<i style='text-align:{alineacion};'>{extraer_valor(valor, 'texto')}</i>\n"
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