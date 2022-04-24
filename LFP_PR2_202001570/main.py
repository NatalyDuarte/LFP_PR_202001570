from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import QPixmap
from analizadorlexico import analizadorlexico

class Ventana(QMainWindow):
    global partidos_arre
    partidos_arre=[]
    def __init__(self):
        super().__init__()
        loadUi("princi.ui", self)
        global anali
        anali= analizadorlexico()
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
        self.pushButton.clicked.connect(self.send)
        self.pushButton_4.clicked.connect(self.anali)
        self.pushButton_3.clicked.connect(self.borrarerro)
        self.pushButton_5.clicked.connect(self.borrartoke)
        self.pushButton_2.clicked.connect(self.reporerrores)

    def lectura(self,ruta):
        archi=open(ruta, 'r')
        conte=archi.read()
        archi.close()
        return conte

    def send(self):
        archivo = self.lineEdit.text()
        anali.analizar(archivo)
        anali.imprimir()
        self.textEdit.append('\n'+'YOU: '+archivo)

    def anali(self):
        anali.HTMLTOKENS()
    
    def borrarerro(self):
        anali.limpiarerrores()

    def borrartoke(self):
        anali.limpiartokens()
    
    def reporerrores(self):
        anali.HTMLERRORES()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana()
    GUI.show()
    sys.exit(app.exec_())