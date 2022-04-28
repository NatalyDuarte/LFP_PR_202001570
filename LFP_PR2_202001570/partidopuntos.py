class partidopuntos:
    def __init__(self, partido, puntos):
        self.partido = partido
        self.puntos = puntos

    def getPartido(self):
        return self.partido

    def getPuntos(self):
        return self.puntos

    def setPartido(self, partido):
        self.partido = partido

    def setPuntos(self, puntos):
        self.puntos = puntos

    def __repr__(self):
        return "Nombre del partido:"+ self.partido +" Puntos:" + str(self.puntos)