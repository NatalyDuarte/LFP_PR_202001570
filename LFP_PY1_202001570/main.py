from distutils.log import error
from email import message
from secrets import token_urlsafe
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tokens import tokens
from error import error
import webbrowser

def Inicio():
    global token
    token =[]
    token.append(tokens("coma",",","1","2"))
    global errores
    errores =[]
    errores.append(error("coma","se encuentra mal ubicada","1","2"))
    root=Tk()
    root.title("Proyecto 1")
    root.geometry("1000x600")
    root.config(bg="PeachPuff4")
    
    frame=Frame(root,width=1000, height=600)
    frame.config(bg="PeachPuff4")
    frame.pack()

    global combito
    combito=ttk.Combobox(frame)
    combito.place(x=500, y=10)
    combito['values']=('Reporte de tokens','Reporte de errores','Manual de Usuario','Manual Tecnico')

    botonanali=Button(frame, width=13,height=3, text="Cargar Archivo", bg="coral", command=lectura)
    botonanali.grid(row=0, column=0)

    botonobte=Button(frame, width=13,height=3, text="Cargar opcion", bg="coral", command=obtener)
    botonobte.grid(row=0, column=2)

    global areadetexto
    areadetexto=Text(frame)
    areadetexto.grid(row=1, column=1, padx=50, pady=50)

    scroll=Scrollbar(frame,command=areadetexto.yview)
    scroll.place(relx=0.95,rely=0.2,relheight=0.2)

    botonanali=Button(frame, width=13,height=3, text="Analizar", bg="violet")
    botonanali.grid(row=2, column=1)

    root.mainloop()

def lectura():
    global rutarecibida
    archi=filedialog.askopenfilename(filetypes=[("Archivos FORM", ".form .FORM")])
    rutarecibida=ArchivoMemoria(archi)
    areadetexto.insert(END,rutarecibida)

def ArchivoMemoria(rutarchi):
    try:
        with open(rutarchi, encoding='utf-8') as file:
            datarchi = file.read()
            return datarchi
    except:
        messagebox.showwarning("Alert","No se pudo abrir el archivo")

def obtener():
    if str(combito.get())=="Reporte de tokens":
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
        for f in range(0,len(token)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+token[f-1].tipo+"</center></td><td><center>"+token[f-1].lexema+"</center></td><td><center>"+token[f-1].fila+"</center></td><td><center>"+token[f-1].columna+"</center></td></tr>"
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
    elif str(combito.get())=="Reporte de errores":
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de Errores</title>
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
        for f in range(0,len(errores)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+errores[f-1].tipo+"</center></td><td><center>"+errores[f-1].descripcion+"</center></td><td><center>"+errores[f-1].fila+"</center></td><td><center>"+errores[f-1].columna+"</center></td></tr>"
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
        doc = open('ReporteError.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('ReporteError.html')
    elif str(combito.get())=="Manual de Usuario":
        webbrowser.open_new_tab('Manual_de_usuario.pdf')
    elif str(combito.get())=="Manual Tecnico":
        webbrowser.open_new_tab('Manual_tecnico.pdf')


if __name__ == '__main__':
    Inicio()