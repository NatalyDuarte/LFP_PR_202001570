from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import QPixmap
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
from tokens import tokens
from error import error
from analizador1 import analizador1

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ventana.ui", self)
        self.pushButton.clicked.connect(self.lectura)
        self.pushButton_2.clicked.connect(self.item)
        self.pushButton_3.clicked.connect(self.analizardoc)
        self.pushButton_4.clicked.connect(self.salir)
    
    def salir(self):
        sys.exit(1)

    def analizardoc(self):
        global anali
        anali= analizador1()
        archivo = self.plainTextEdit.toPlainText()
        anali.analizar(archivo)
        anali.imprimir()
        #anali.CrearHtml()

    def lectura(self):
        global rutarecibida
        archi=filedialog.askopenfilename(filetypes=[("Archivos FORM", ".form .FORM")])
        rutarecibida=self.ArchivoMemoria(archi)
        self.plainTextEdit.setPlainText(rutarecibida)      

    def ArchivoMemoria(self, rutarchi):
        try:
            with open(rutarchi, encoding='utf-8') as file:
                datarchi = file.read()
                return datarchi
        except:
            messagebox.showwarning("Alert","No se pudo abrir el archivo")

    def item(self):
        itms= self.comboBox.currentText()
        if str(itms)=="Reporte de tokens":
            anali.HTMLTOKENS()
        elif str(itms)=="Reporte de errores":
            anali.HTMLERRORES()
        elif str(itms)=="Manual de Usuario":
            webbrowser.open_new_tab('Manual_de_usuario.pdf')
        elif str(itms)=="Manual Tecnico":
            webbrowser.open_new_tab('Manual_tecnico.pdf')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana()
    GUI.show()
    sys.exit(app.exec_())