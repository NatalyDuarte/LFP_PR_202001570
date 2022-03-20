from tokens import tokens
from error import error
from valorees import valorees
import re
import webbrowser
from formulariohtml import formulariohtml

class analizadorr:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []

    def analizar(self, codigo):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []
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
                if cade== "~":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Virgulilla',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1
                elif cade == ">":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Signo_mayor',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1
                elif cade == "[":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Corchete_Abrir',buffer, fila, columna))
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
                elif cade == ":":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Dos_puntos',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1
                elif cade == ",":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Coma',buffer, fila, columna))
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
                elif re.search('[a-zA-Z]',cade):
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
                elif cade == '\n':
                    fila+=1
                    columna=1
                    i+=1
                elif cade == '\t' or cade == ' ':
                    columna+=1
                    i+=1
                elif cade=='-':
                    columna +=1
                    i+=1
                #validacion del centinela
                elif cade == centinela:
                    break
                else:
                    #errores
                    buffer=''
                    self.listaErrores.append(error('Error Léxico', cade, fila, columna))
                    columna+=1
                    i+=1
            #Palabras reservadas
            elif estado == 1:
                if re.search('[a-zA-Z]',cade):
                    buffer+=cade
                    columna+=1
                    estado=1
                    i+=1
                else:
                    global tipotoken
                    tipotoken=""
                    if buffer.lower()=="formulario":
                        tipotoken="FORMULARIO"
                    elif buffer.lower()=="tipo":
                        tipotoken="TIPO"
                    elif buffer.lower()=="valor":
                        tipotoken="VALOR"
                    elif buffer.lower()=="fondo":
                        tipotoken="FONDO"
                    elif buffer.lower()=="nombre":
                        tipotoken="NOMBRE"
                    elif buffer.lower()=="valores":
                        tipotoken="VALORES"
                    elif buffer.lower()=="evento":
                        tipotoken="EVENTO"
                    else: 
                        tipotoken="IDENTIFICADOR"
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
                elif cade == '\'':
                    buffer = buffer.replace("\'","")
                    global arreglo1
                    arreglo1 = buffer.split(",")
                    for m in range(0, len(arreglo1),2):
                        self.listaTokens.append(tokens('Cadena',arreglo1[m], fila, columna))    
                    estado=0
                    buffer=''
                    i+=1
                else:
                    buffer+=cade
                    columna+=1
                    estado=2
                    i+=1
    
    def agregarlisthtml(self):
        global tipo
        global valor
        global fondo
        global evento
        global nombre
        global valoress
        tipo=" "
        fondo=" "
        evento=" "
        valor =" "
        nombre=" "
        valoress=[]
        componente= False
        i=0
        while i<len(self.listaTokens):
            if self.listaTokens[i].getTipo() == "Signo_menor":
                componente = True
            elif self.listaTokens[i].getTipo() == "TIPO":
                    tipo=self.listaTokens[i+2].lexema
            elif self.listaTokens[i].getTipo() == "VALOR":
                    valor=self.listaTokens[i+2].lexema
            elif self.listaTokens[i].getTipo() == "FONDO":
                    fondo=self.listaTokens[i+2].lexema
            elif self.listaTokens[i].getTipo() == "VALORES":
                    while self.listaTokens[i].getLexema() != "]":
                            if self.listaTokens[i].getLexema() !="[" and self.listaTokens[i].getLexema() != ":" and self.listaTokens[i].getLexema() != "," and self.listaTokens[i].getTipo() != "VALORES":
                                valoress.append(valorees(self.listaTokens[i].getLexema())) 
                            i+=1
            elif self.listaTokens[i].getTipo() == "NOMBRE":
                nombre=self.listaTokens[i+2].lexema
            elif self.listaTokens[i].getTipo() == "EVENTO":
                evento=self.listaTokens[i+2].lexema 
            elif self.listaTokens[i].getTipo() == "Signo_mayor":
                if componente == True:
                    self.listaHtml.append(formulariohtml(tipo, valor ,fondo, valoress, evento,nombre))
                componente= False
            i+=1
        
        
                
    def imprimir(self):
        print("\n\n==========Lista tokens===============")
        for i in self.listaTokens:
            i.strToken()

        print("\n\n==========Lista errores===============")
        for o in self.listaErrores:
            o.strError()

        print("\n\n==========Lista HTML===============")
        for u in self.listaHtml:
            u.__repr__()

    def HTMLERRORES(self):
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
        doc = open('ReporteError.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('ReporteError.html')

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
    
    def CrearHtml(self):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Formulario</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                <meta charset="utf-8">
                <meta name="html" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	            </head>
                <body>
                <div class="container">"""
        for f in range(len(self.listaHtml)):
            if(self.listaHtml[f].tipo=="etiqueta"):
                texto1 = texto1 + "<label>"+self.listaHtml[f].valor+"</label><br>&nbsp;"
            elif(self.listaHtml[f].tipo=="texto"):
                texto1 = texto1 + " <input type=\"text\" id=\""+self.listaHtml[f].valor+"\"placeholder=\""+self.listaHtml[f].fondo+"\"/><br>"
            elif(self.listaHtml[f].tipo=="grupo-radio"):
                if(self.listaHtml[f].getNombre()!=" "):
                    texto1 = texto1 + "<label>"+self.listaHtml[f].getNombre() +": </label>&nbsp;"
                for u in range(0,len(valoress)):
                    texto1 = texto1 + """<div class="form-check form-check-inline">
                                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value=\""""+self.listaHtml[f].valor+"""\">
                                            <label class="form-check-label" for="inlineRadio1">"""+valoress[u-1].valor+"""</label>
                                        </div>"""
            elif(self.listaHtml[f].tipo=="grupo-option"):
                for o in range(0,len(valoress)):
                  texto1 = texto1 + """<select name=\"select\">
                  <option>"""+valoress[o-1].valor+"""</option>
                  </select>"""
            elif(self.listaHtml[f].tipo=="boton"):
                #texto1 = texto1 +"<button type=\"button\" class=\"btn btn-info\"  value=\""+self.listaHtml[f].valor+"\">"+self.listaHtml[f].fondo+"</button>"
                if(self.listaHtml[f].evento=="entrada"):
                    texto1 = texto1 + "<input type=\"button\"  value=\""+self.listaHtml[f].valor+"\"placeholder=\""+self.listaHtml[f].fondo+"\"onclick=\"Evaluar()\"/><br>"
                elif(self.listaHtml[f].evento=="entrada"):
                    texto1 = texto1 + "<input type=\"button\"  value=\""+self.listaHtml[f].valor+"\"placeholder=\""+self.listaHtml[f].fondo+"\"onclick=\"Evaluar1()\"/><br>"
                else:
                    entrada=" "
                    info=" "
        texto1= texto1+"""</div></body>
                         </html>
                        """
        doc = open('Formulario.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('Formulario.html')
