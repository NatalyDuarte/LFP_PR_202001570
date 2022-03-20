class formulariohtml:
    def __init__(self, tipo, valor ,fondo, listavalores, evento,nombre):
        self.tipo=tipo
        self.valor=valor
        self.fondo=fondo
        self.listavalores=listavalores
        self.evento=evento
        self.nombre = nombre

    def __repr__(self):
        print("\n=================================")
        print("Tipo:"+self.tipo)
        print("Valor:  "+self.valor)
        print("Fondo:  "+self.fondo)
        print("Evento: "+self.evento)
        print("Nombre: "+self.nombre)
