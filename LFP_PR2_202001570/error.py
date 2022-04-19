class error:
    def __init__(self,tipo, descripcion, lexema, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.lexema = lexema 
        self.fila = fila
        self.columna = columna-len(descripcion)

    def strError(self):
        print("\n=================================")
        print("Tipo:" +self.tipo)
        print("Descripción:  "+self.descripcion)
        print("Lexema: "+str(self.lexema))
        print("Fila:  " +str(self.fila))
        print("Columna: "+str(self.columna))