class tokens:
    def __init__(self, tipo,lexema, fila, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.columna = columna-1

    def getTipo (self):
        return self.tipo

    def getLexema (self):
        return self.lexema
    
    def strToken(self):
        print("\n=================================")
        print("Tipo:" +self.tipo)
        print("Lexema:  "+self.lexema)
        print("Fila:  " +str(self.fila))
        print("Columna: "+str(self.columna))