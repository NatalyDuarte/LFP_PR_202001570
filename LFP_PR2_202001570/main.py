from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import QPixmap

class Ventana(QMainWindow):
    global partidos_arre
    partidos_arre=[]
    def __init__(self):
        super().__init__()
        loadUi("princi.ui", self)
        archivo=self.lectura("LaLigaBot-LFP.csv")
        partidos= archivo.split("\n")
        for partid in partidos:
            datos=partid.split(",")
            p={
                "Fecha":datos[0],
                "Temporada":datos[1],
                "Jornada":datos[2],
                "Equipo1":datos[3],
                "Equipo2":datos[4],
                "Goles1":datos[5],
                "Goles2":datos[6],
            }
            partidos_arre.append(p)
        partidos_arre.pop(0)

    def lectura(self,ruta):
        archi=open(ruta, 'r')
        conte=archi.read()
        archi.close()
        return conte
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana()
    GUI.show()
    sys.exit(app.exec_())