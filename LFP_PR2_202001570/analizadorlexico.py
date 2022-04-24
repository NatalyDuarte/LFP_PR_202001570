from tokens import tokens
from error import error
import re
import webbrowser
class analizadorlexico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        #self.listaHtml = []

    def limpiartokens(self):
        self.listaTokens = []

    def limpiarerrores(self):
        self.listaErrores = []

    def analizar(self, codigo):
        global cod
        cod= codigo
        #self.listaHtml = []
        # VARIABLES
        fila = 1
        columna = 1
        buffer = ''
        centinela = '$'
        estado = 0
        codigo += centinela
        # AUTOMATA
        i = 0
        while i < len(codigo):
            cade= codigo[i]
            #ESTADO 0
            if estado == 0:
                #Signos/Simbolos
                if cade == "[":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Corchete_Abrir',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1               
                if cade == ">":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Signo_mayor',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1      
                elif cade == "<":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Signo_menor',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1                     
                elif cade == "]":
                    columna+=1
                    buffer+= cade
                    self.listaTokens.append(tokens('Corchete_Cerrar',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1
                #letras/palabras reservadas
                elif re.search('[A-Z]',cade):
                    columna+=1
                    buffer+= cade
                    estado=1
                    i+=1
                #cadena
                elif cade=='"' or cade == '\'':
                    columna+=1
                    buffer+=cade
                    estado=2
                    i+=1
                #numero 
                elif re.search('[0-9]',cade):
                    columna+=1
                    buffer+= cade
                    estado=3
                    i+=1                
                #archivo
                elif re.search('[A-Za-z0-9]',cade):
                    columna+=1
                    buffer+= cade
                    estado=4
                    i+=1
                elif cade == '\n':
                    fila+=1
                    columna=1
                    i+=1
                elif cade == '\t' or cade == ' 'or cade == '\r':
                    columna+=1
                    i+=1  
                elif cade=='-':
                    columna+=1
                    buffer+= cade
                    estado=1
                    i+=1
                elif cade==':':
                    columna +=1
                    i+=1
                #validacion del centinela
                elif cade == centinela:
                    break
                else:
                    #errores
                    buffer=''
                    columna+=1
                    self.listaErrores.append(error('Error Léxico', cade, fila, columna))
                    i+=1
            #Palabras reservadas
            elif estado == 1:
                if re.search('[a-z]',cade):
                    buffer+=cade
                    columna+=1
                    estado=1
                    i+=1
                elif re.search('[A-Z]',cade):
                    buffer+=cade
                    columna+=1
                    estado=1
                    i+=1
                else:
                    global tipotoken
                    tipotoken=""
                    if buffer=="RESULTADO":
                        tipotoken="RESULTADO"
                    elif buffer=="VS":
                        tipotoken="VS"
                    elif buffer=="TEMPORADA":
                        tipotoken="TEMPORADA"
                    elif buffer=="JORNADA":
                        tipotoken="JORNADA"
                    elif buffer=="GOLES":
                        tipotoken="GOLES"
                    elif buffer=="LOCAL":
                        tipotoken="LOCAL"
                    elif buffer=="VISITANTE":
                        tipotoken="VISITANTE"
                    elif buffer=="TOTAL":
                        tipotoken="TOTAL"
                    elif buffer=="TABLA":
                        tipotoken="TABLA"
                    elif buffer=="TABLA TEMPORADA":
                        tipotoken="TABLA TEMPORADA"
                    elif buffer=="PARTIDOS":
                        tipotoken="PARTIDOS"
                    elif buffer=="TOP":
                        tipotoken="TOP"
                    elif buffer=="SUPERIOR":
                        tipotoken="SUPERIOR"
                    elif buffer=="INFERIOR":
                        tipotoken="INFERIOR"
                    elif buffer=="ADIOS":
                        tipotoken="ADIOS"
                    elif buffer=="-f":
                        tipotoken="-f"
                    elif buffer=="-ji":
                        tipotoken="-ji"
                    elif buffer=="-n":
                        tipotoken="-n"
                    elif buffer=="-jf":
                        tipotoken="-jf"
                    elif buffer=="-":
                        tipotoken="Guion"
                    elif buffer=="YOU":
                        tipotoken="IDENTIFICADOR"
                    else: 
                        estado=5
                    self.listaTokens.append(tokens(tipotoken,buffer, fila, columna))
                    buffer = ''
                    estado=0  
            #Cadenas                 
            elif estado == 2:
                if cade == '"':
                    buffer = buffer.replace("\"","")
                    self.listaTokens.append(tokens('Cadena',buffer, fila, columna))
                    estado=0
                    buffer=''
                    i+=1
                else:
                    buffer+=cade
                    columna+=1
                    estado=2
                    i+=1
            #Numeros
            elif estado == 3:
                if re.search('[0-9]',cade):
                    buffer+=cade
                    columna+=1
                    estado=3
                    i+=1 
                else:
                    if re.search(r'\d\d\d\d',buffer):
                        self.listaTokens.append(tokens('Fecha',buffer, fila, columna))
                    elif re.search(r'\d\d',buffer):
                        self.listaTokens.append(tokens('Número',buffer, fila, columna))
                    elif re.search(r'\d',buffer):
                        self.listaTokens.append(tokens('Número',buffer, fila, columna))
                    else:
                        self.listaTokens.append(tokens('Número',buffer, fila, columna))                  
                    buffer=''
                    estado=0
            #Instruccion
            elif estado == 4:
                if re.search('[A-Za-z0-9]',cade):
                    buffer+=cade
                    columna+=1
                    estado=4
                    i+=1 
                else:
                    self.listaTokens.append(tokens('Archivo',buffer, fila, columna))
                    estado=0
                    buffer=''
                    i+=1
                
    def imprimir(self):
        print("\n\n==========Lista tokens===============")
        for i in self.listaTokens:
            i.strToken()

        print("\n\n==========Lista errores===============")
        for o in self.listaErrores:
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
        for f in range(0,len(self.listaErrores)):
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+self.listaErrores[f-1].tipo+"</center></td><td><center>"+self.listaErrores[f-1].descripcion+"</center></td><td><center>"+str(self.listaErrores[f-1].fila)+"</center></td><td><center>"+str(self.listaErrores[f-1].columna)+"</center></td></tr>"
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