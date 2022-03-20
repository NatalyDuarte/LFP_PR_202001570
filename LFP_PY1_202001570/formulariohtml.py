class formulariohtml:
    def __init__(self, tipo, valor ,fondo, listavalores, evento,nombre):
        self.tipo=tipo
        self.valor=valor
        self.fondo=fondo
        self.listavalores=listavalores
        self.evento=evento
        self.nombre = nombre
    def getTipo (self):
        return self.tipo
    def getValor (self):
        return self.valor
    def getFondo (self):
        return self.fondo
    def getListavalores (self):
        return self.listavalores
    def getEvento (self):
        return self.evento
    def getNombre (self):
        return self.nombre

    def __repr__(self):
        print("\n=================================")
        print("Tipo:"+self.tipo)
        print("Valor:"+self.valor)
        print("Fondo:"+self.fondo)
        print("Evento:"+self.evento)
        print("Nombre:"+self.nombre)
