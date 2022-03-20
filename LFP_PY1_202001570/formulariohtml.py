class formulariohtml:
    def __init__(self, tipo, valor ,fondo, listavalores, evento,nombre):
        self.tipo=tipo
        self.valor=valor
        self.fondo=fondo
        self.listavalores=listavalores
        self.evento=evento
        self.nombre = nombre

    def __repr__(self):
        print(self.tipo+" "+self.valor+" "+self.fondo+" "+self.evento+" "+self.nombre)
