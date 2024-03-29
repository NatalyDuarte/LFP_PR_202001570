from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.uic import loadUi
import sys
from PyQt5.QtGui import QPixmap
from analizadorlexico import analizadorlexico
from analizadorsintactico import analizadorsintactico
from tokens import tokens
from error import error
import webbrowser
from tkinter import messagebox
class Ventana(QMainWindow):
    def __init__(self):
        self.resultado= []
        self.partidos_arre=[]
        self.listaTokens = []
        self.listaErroresLex = []
        self.listaErroresSin = []
        self.i=0
        super().__init__()
        loadUi("princi.ui", self)
        global anali, analisin
        anali= analizadorlexico()
        analisin = analizadorsintactico()
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
            self.partidos_arre.append(p)
        self.partidos_arre.pop(0)
        self.imprimir()
        self.pushButton.clicked.connect(self.send)
        self.pushButton_4.clicked.connect(self.anali)
        self.pushButton_3.clicked.connect(self.borrarerro)
        self.pushButton_5.clicked.connect(self.borrartoke)
        self.pushButton_2.clicked.connect(self.reporerrores)
        self.pushButton_6.clicked.connect(self.abrirmanu)
        self.pushButton_7.clicked.connect(self.abrirmanu1)
    
    def abrirmanu(self):
        webbrowser.open_new_tab('Manual_de_usuario.pdf')

    def abrirmanu1(self):
        webbrowser.open_new_tab('Manual_tecnico.pdf')

    def lectura(self,ruta):
        archi=open(ruta, 'r')
        conte=archi.read()
        #archi.close()
        return conte

    def send(self):
        archivo = self.lineEdit.text()
        anali.analizar(archivo,self.listaTokens,self.listaErroresLex)
        analisin.analizar(self.listaTokens, self.listaErroresSin,self.partidos_arre,self.resultado)
        if len(self.listaErroresSin)==0:
            self.textEdit.append('\n'+'YOU: '+archivo)
            if len(self.resultado)>0:
                self.textEdit.append('\n'+'BOT: '+str(self.resultado[0]))
            else:
                self.textEdit.append('\n'+'BOT: No se encontraron resultados') 
        else:
            for o in range(len(self.listaErroresSin)):
                if self.listaErroresSin[o].tipo==None:
                    self.textEdit.append('\n'+'YOU: '+archivo)
                    if len(self.resultado)>0:
                        self.textEdit.append('\n'+'BOT: '+str(self.resultado[0]))
                    else:
                        self.textEdit.append('\n'+'BOT: No se encontraron resultados')
                else:
                    messagebox.showwarning("Alert","La sintaxis no es correcta")
        if len(self.resultado)>0:
            if self.resultado[0]=="ADIOS":
                messagebox.showwarning("Alert","ADIOS")
                sys.exit(1)
        self.imprimir()
        

    def anali(self):
        self.HTMLTOKENS()
    
    def borrarerro(self):
        self.listaErroresLex = []
        self.listaErroresSin = []
        self.resultado = []
        self.imprimir()

    def borrartoke(self):
        self.listaTokens = []
        self.resultado = []
        self.imprimir()
    
    def reporerrores(self):
        self.HTMLERRORES()
        self.HTMLERRORES1()
    
    def imprimir(self):
        print("\n\n==========Lista tokens===============")
        for i in self.listaTokens:
            i.strToken()

        print("\n\n==========Lista errores Lexicos===============")
        for o in self.listaErroresLex:
            o.strError()

        print("\n\n==========Lista errores Sintacticos===============")
        for o in self.listaErroresSin:
            o.strError()

    def HTMLERRORES(self):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de Errores Lexicos</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	            <link rel="stylesheet" href="css/style.css">
                <H1><font color="Olive" face="Comic Sans MS,arial">Nataly Saraí Guzmán Duarte 202001570</font></H1>
	            </head>
	            <body style="background-color:pink;">
	                <section class="ftco-section">
		            <div class="container">
			            <div class="row justify-content-center">
				            <div class="col-md-6 text-center mb-5">
					            <h2 class="heading-section">Tabla de Errores</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Tipo de token</th>
						                <th>Lexema</th>
						                <th>Fila</th>
						                <th>Columna</th>
						                </tr>
						            </thead>"""
        for f in range(0,len(self.listaErroresLex)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+self.listaErroresLex[f-1].tipo+"</center></td><td><center>"+self.listaErroresLex[f-1].descripcion+"</center></td><td><center>"+str(self.listaErroresLex[f-1].fila)+"</center></td><td><center>"+str(self.listaErroresLex[f-1].columna)+"</center></td></tr>"
        texto= """</tr>
                 </tbody>
				    </table>
					</div>
				</div>
			</div>
		</div>
        """
        conti="""</section>
	            </body>
            </html>
            """
        texto1=texto1+texto+conti
        doc = open('ReporteErrorLex.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('ReporteErrorLex.html')

    def HTMLERRORES1(self):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de Errores Lexicos</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	            <link rel="stylesheet" href="css/style.css">
                <H1><font color="Olive" face="Comic Sans MS,arial">Nataly Saraí Guzmán Duarte 202001570</font></H1>
	            </head>
	            <body style="background-color:pink;">
	                <section class="ftco-section">
		            <div class="container">
			            <div class="row justify-content-center">
				            <div class="col-md-6 text-center mb-5">
					            <h2 class="heading-section">Tabla de Errores</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Tipo de token</th>
						                <th>Lexema</th>
						                <th>Fila</th>
						                <th>Columna</th>
						                </tr>
						            </thead>"""
        for f in range(0,len(self.listaErroresSin)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+self.listaErroresSin[f-1].tipo+"</center></td><td><center>"+self.listaErroresSin[f-1].descripcion+"</center></td><td><center>"+str(self.listaErroresSin[f-1].fila)+"</center></td><td><center>"+str(self.listaErroresSin[f-1].columna)+"</center></td></tr>"
        texto= """</tr>
                 </tbody>
				    </table>
					</div>
				</div>
			</div>
		</div>
        """
        conti="""</section>
	            </body>
            </html>
            """
        texto1=texto1+texto+conti
        doc = open('ReporteErrorSin.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('ReporteErrorSin.html')

    def HTMLTOKENS(self):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de tokens</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <link href='https://fonts.googleapis.com/css?family=Roboto:400,100,300,700' rel='stylesheet' type='text/css'>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
	            <link rel="stylesheet" href="css/style.css">
                <H1><font color="Olive" face="Comic Sans MS,arial">Nataly Saraí Guzmán Duarte 202001570</font></H1>
	            </head>
	            <body style="background-color:pink;">
	                <section class="ftco-section">
		            <div class="container">
			            <div class="row justify-content-center">
				            <div class="col-md-6 text-center mb-5">
					            <h2 class="heading-section">Tabla de tokens</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Tipo</th>
						                <th>Lexema</th>
						                <th>Fila</th>
						                <th>Columna</th>
						                </tr>
						            </thead>"""
        for f in range(0,len(self.listaTokens)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+self.listaTokens[f-1].tipo+"</center></td><td><center>"+self.listaTokens[f-1].lexema+"</center></td><td><center>"+str(self.listaTokens[f-1].fila)+"</center></td><td><center>"+str(self.listaTokens[f-1].columna)+"</center></td></tr>"
        texto= """</tr>
                 </tbody>
				    </table>
					</div>
				</div>
			</div>
		</div>
        """
        conti="""</section>
	            </body>
            </html>
            """
        texto1=texto1+texto+conti
        doc = open('ReporteTokens.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('ReporteTokens.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana()
    GUI.show()
    sys.exit(app.exec_())