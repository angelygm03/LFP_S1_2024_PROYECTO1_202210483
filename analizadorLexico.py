import re
from lexema import Lexema, Error

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
            elif char in ['=']:
                lexemas.append(Lexema("Igual", char, fila, columna))                     
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
    return lexemas, errores

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