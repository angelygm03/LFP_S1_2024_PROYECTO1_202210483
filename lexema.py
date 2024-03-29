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
