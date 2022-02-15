from sys import flags
from tkinter import *
from tkinter import filedialog
from turtle import title
from Producto import Producto
from Grafica import Grafica
import matplotlib.pyplot as plt
import numpy as np
import re
import webbrowser

def ArchivoMemoria(rutarchi):
    try:
        with open(rutarchi, encoding='utf-8') as file:
            datarchi = file.read()
            #print("\n")
            print(datarchi)
            return datarchi
    except:
        print('No se pudo abrir el archivo porque no existe: ' + rutarchi)

def listavacia (lista):
    return not lista

def AnalisisArchi(archiv,archivo):
    #Buscando el mes
    global mess
    mess = ''
    for i in archiv:
        if i == ' ':
            break
        else:
            mess += i
    print("Mes: ", mess)
    #Buscando el año
    global ano2
    ano=re.findall(r'\d\d\d\d',archiv)
    ano1=ano[0]
    ano2=ano1.replace("["," ")
    print("El año es :", ano2)      
    global ayos
    #ayos = sinayo.split(";")
    #Buscando los productos
    datospara = ''
    para1 = False
    for c in archiv:
        if c == '(':
            para1 = True
            continue
        if c != ')' and para1:
            datospara += c
        elif c == ')':
            break
    j = ''
    for a in datospara:
        if a == ";" or a == "[" or a == "\"" or a == "\n":
            continue
        else:
            j += a
    pruebalista = j.replace("]", ",")
    # CREA UNA LISTA CON LOS DATOS
    arreglo = pruebalista.split(",")
    global producto
    producto = []
    for m in range(0, len(arreglo),3):
        if m == len(arreglo)-1:
            continue
        else:
            ganancia=float(arreglo[m+1])*float(arreglo[m+2])
            producto.append(Producto(arreglo[m], arreglo[m+1], arreglo[m+2],str(ganancia)))
    for produc in producto:
        print(produc)
    #Buscando datos grafica
    #Buscando nombre_______________________________________-
    global nom
    global grafi
    nome=re.findall(r'nombre\s*:\s*"[\w\s,\.]+"',archivo,flags=re.I)
    no1=listavacia(nome)
    if (no1== False):
        nom=nome
        nom1=nom[len(nom)-1]
        nom2=nom1.replace(":",";")
        nom3=nom2.replace("\"\""," " )
        print(nom3)
        # CREA UNA LISTA CON LOS DATOS DE NOMBRE
        arreglo = nom3.split(";")
        grafi = []
        for m in range(0, len(arreglo),2):
            if m == len(arreglo)-1:
                continue
            else:
                no=arreglo[m+1]
                no.lower()
                print(no)
    #Buscando tipo de grafica_______________________________________-
        global tipo
        tip1=re.findall(r'grafica\s*:\s*"[\w\s,\.]+"',archivo,flags=re.I)
        ti1=listavacia(tip1)
        if (ti1== False ):
            tipo=tip1
            tipo1=tipo[len(tipo)-1]
            tipo2=tipo1.replace(":",";")
            print(tipo2)
        # CREA UNA LISTA CON LOS DATOS DE TIPO
            arreglo1 = tipo2.split(";")
            for m in range(0, len(arreglo1),2):
                if m == len(arreglo1)-1:
                 continue
                else:
                    ti=arreglo1[m+1]
                    ti.lower()
                    print(ti)
            #Buscando titulo de grafica_______________________________________-
            global titulo
            tit1=re.findall(r'titulo\s*:\s*"[\w\s,\.]+"',archivo,flags=re.I)
            titu1=listavacia(tit1)
            if (titu1== False):
                titulo=tit1
                titulo1=titulo[len(titulo)-1]
                titulo2=titulo1.replace(":",";")
                print(titulo2)
                # CREA UNA LISTA CON LOS DATOS DE TITULO
                arreglo2 = titulo2.split(";")
                for m in range(0, len(arreglo2),2):
                    if m == len(arreglo2)-1:
                        continue
                    else:
                        titu=arreglo2[m+1]
                        titu.lower()
                        print(titu)
        
            #Buscando titulox de grafica_______________________________________-
            global titulox
            titx1=re.findall(r'titulox\s*:\s*"[\w\s,\.]+"',archivo,flags=re.I)
            titux1=listavacia(titx1)
            if (titux1== False):
                titulox=titx1
                titulox1=titulox[len(titulox)-1]
                titulox2=titulox1.replace(":",";")
                print(titulox2)
                # CREA UNA LISTA CON LOS DATOS DE TITULO
                arreglo3 = titulox2.split(";")
                for m in range(0, len(arreglo3),2):
                    if m == len(arreglo3)-1:
                        continue
                    else:
                        titux=arreglo3[m+1]
                        titux.lower()
                        print(titux)
            #Buscando tituloy de grafica_______________________________________-
            global tituloy
            tity1=re.findall(r'tituloy\s*:\s*"[\w\s*,\.]+"',archivo,flags=re.I)
            tituy1=listavacia(tity1)
            if (tituy1== False):
                tituloy=tity1
                tituloy1=tituloy[len(tituloy)-1]
                tituloy2=tituloy1.replace(":",";")
                print(tituloy2)
                # CREA UNA LISTA CON LOS DATOS DE TITULO
                arreglo4 = tituloy2.split(";")  
                for m in range(0, len(arreglo4),2):
                    if m == len(arreglo4)-1:
                        continue
                    else:
                        tituy=arreglo4[m+1]
                        tituy.lower()
                        print(tituy)
            grafi.append(Grafica(no,ti, titu, titux, tituy))
            print("comprobando")
            for i in grafi:
                print(i)
               
        else:
            print("Error el archivo no contiene los campos obligatorios")
    else:
        print("Error el archivo no contiene los campos obligatorios")
    Graficar(producto,grafi)
            
def Graficar(produ,gra):
     for f in gra :
        if(f.grafica == "\"pie\"" or f.grafica == "\"pastel\"" ):
            arrex=[]
            for g in produ :
                arrex.append(g.ganancia)
            colors = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(arrex)))
            fig, ax = plt.subplots()
            ax.pie(arrex, colors=colors, radius=3, center=(4, 4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),ylim=(0, 8), yticks=np.arange(1, 8))
            plt.show()
        if(f.grafica == "\"Barras\"" ):
            arrx=[]
            arry=[]
            for g in produ :
                arrx.append(g.producto)
                arry.append(g.ganancia)
            si=np.arange(len(arrx))
            fig1, ax1 = plt.subplots()
            recx=ax1.bar(si - 0.5/2,arry,0.5,edgecolor="Red")
            #ax1.bar(arrx, arry, width=1, edgecolor="Red", linewidth=0.9)
            ax1.set_title(grafi.titulo)
            ax1.set_xlabel(grafi.titulox)
            ax1.set_ylabel(grafi.tituloy)
            ax1.set_xticks(si,arrx)
            ax1.bar_label(recx,padding=4)
            fig1.tight_layout()
            plt.savefig(grafi.nombre+".png")
            plt.show()
        if(f.grafica == "\"lineas\"" ):
            arx=[]
            ary=[]
            for g in produ :
                arx.append(g.producto)
                ary.append(g.ganancia)
"""
            if(f.instruccion!="titulo"):
                plt.title(f.resu)
            else:
                plt.title("Reporte de Ventas_"+mess+"-"+ano2)
            if(f.instruccion!="titulox"):
                plt.xlabel(f.resu)
            else:
                plt.xlabel(" ") 
            if(f.instruccion!="tituloy"):
                plt.ylabel(f.resu)
            else:
                plt.ylabel(" ") 
            plt.legend()
            plt.show
        """

 #_________________________________________________________________________________
def Ordenamiento(arreglo):
    for f in range(len(arreglo)-1, 0, -1):
        for i in range(f):
            if float(arreglo[i].ganancia) > float(arreglo[i+1].ganancia):
                temp = arreglo[i]
                arreglo[i] = arreglo[i+1]
                arreglo[i+1] = temp

def OrdenamientoporVendido(arreglo):
    for f in range(len(arreglo)-1, 0, -1):
        for i in range(f):
            if float(arreglo[i].cantidad) > float(arreglo[i+1].cantidad):
                temp = arreglo[i]
                arreglo[i] = arreglo[i+1]
                arreglo[i+1] = temp

def Reporte():
    texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de productos</title>
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
					            <h2 class="heading-section">Tabla de productos</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Nombre del producto</th>
						                <th>Precio Unitario</th>
						                <th>Cantidad de unidades vendidas</th>
						                <th>Ganancias generadas</th>
						                </tr>
						            </thead>"""
    Ordenamiento(producto)
    for f in range(len(producto), 0, -1):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+producto[f-1].producto+"</center></td><td><center>Q."+producto[f-1].preciouni+"</center></td><td><center>"+producto[f-1].cantidad+"</center></td><td><center>Q."+producto[f-1].ganancia+"</center></td></tr>"
    texto= """</tr>
                 </tbody>
				    </table>
					</div>
				</div>
			</div>
		</div>
        """
    OrdenamientoporVendido(producto)    
    texto=texto+"<H4><font color=\"Black\" face=\"Comic Sans MS,arial\"><center>*El producto mas vendido es:"+producto[(len(producto)-1)].producto+" Con"+producto[(len(producto)-1)].cantidad+" ventas. Y ganancia de Q."+producto[(len(producto)-1)].ganancia+"</font></H1>"
    texto=texto+"<H4><font color=\"Black\" face=\"Comic Sans MS,arial\"><center>*El producto menos vendido es:"+producto[0].producto+" Con"+producto[0].cantidad+" ventas. Y ganancia de Q."+producto[0].ganancia+"</font></H1>"
    conti="""</section>
	            </body>
            </html>
            """
    texto1=texto1+texto+conti
    doc = open('Reporte.html','wb')
    doc.write(bytes(texto1,"'utf-8'"))
    doc.close()
    webbrowser.open_new_tab('Reporte.html')


rutarecibida= None
rutarecibida2= None
instru="""
===============MENU================
|1. Cargar Data                   |
|2. Cargar Instrucciones          |
|3. Analizar                      |
|4. Reportes                      |
|5. Salir                         |
===================================
"""
hasta =True
while hasta ==True:
    print(instru)
    print("Digite su opcion: ")
    opc=int(input(">  "))
    ra=Tk()
    if opc == 1:
        archi=filedialog.askopenfilename(filetypes=[("Archivos DATA", ".data .DATA")])
        print("\n Primer archivo procesado exitosamente")
        rutarecibida=ArchivoMemoria(archi)
    elif opc == 2:
        archi2=filedialog.askopenfilename(filetypes=[("Archivos LFP", ".lfp .LFP")])
        print("\n Segundo archivo procesado exitosamente")
        rutarecibida2=ArchivoMemoria(archi2)
    elif opc == 3:
        if (rutarecibida != None and rutarecibida2 != None):
            print("Analizando....")
            AnalisisArchi(rutarecibida,rutarecibida2)

        else:
            print("No se encontro ningun archivo!")
            Menu()
    elif opc == 4:
            if(producto!=None):
                Reporte()
                print("Reporte creado con exito")
            else:
                print("Error al Crear el reporte")
    elif opc == 5:
        print("Hasta pronto")
        hasta = False
    else:
        print("Digito incorrecto")



