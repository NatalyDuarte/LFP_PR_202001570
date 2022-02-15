class Grafica:
    def __init__(self, nombre, grafica, titulo, titulox, tituloy):
        self.nombre = nombre
        self.grafica = grafica
        self.titulo = titulo
        self.titulox = titulox
        self.tituloy = tituloy

    def getNombre (self):
        return self.nombre

    def getGrafica (self):
        return self.grafica

    def getTitulo (self):
        return self.titulo

    def getTituloX (self):
        return self.titulox

    def getTituloY (self):
        return self.tituloy

    def setNombre (self, nombre):
        self.nombre= nombre

    def setGrafica (self, grafica):
        self.grafica= grafica

    def setTitulo (self, titulo):
        self.titulo=titulo

    def setTituloX (self, titulox):
        self.titulox=titulox

    def setTituloY (self, tituloy):
        self.tituloy=tituloy

    def __repr__(self):
        return "Nombre:"+ self.nombre +" Grafica:" + self.grafica +" Titulo:" + self.titulo +" TituloX:" + self.titulox +" TituloY:" + self.tituloy