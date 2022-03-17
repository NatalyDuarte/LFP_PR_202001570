class tokens:
    def __init__(self, tipo,lexema, fila, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.columna = columna-len(lexema)

    def strToken(self):
        print("\n=================================")
        print("Tipo:" +self.tipo)
        print("Lexema:  "+self.lexema)
        print("Fila:  " +str(self.fila))
        print("Columna: "+str(self.columna))