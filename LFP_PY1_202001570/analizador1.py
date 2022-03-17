from tokens import tokens
from error import error
from html import html
from valorees import valorees
import re
import webbrowser

class analizador1:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []

    def analizar(self, codigo):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []
        global valoress
        valoress=[]
        valoress.append(valorees("Masculino"))
        valoress.append(valorees("Femenino"))
        self.listaHtml.append(html("etiqueta","nombre",""," "," "," "))
        self.listaHtml.append(html("texto","nombre","Ingrese nombre"," "," "," "))
        self.listaHtml.append(html("grupo-radio","","Ingrese nombre",valoress," ","nombre"))

        # VARIABLES
        fila = 1
        columna = 1
        buffer = ''
        centinela = '$'
        estado = 0
        codigo += str(centinela)

        # AUTOMATA
        i = 0
        n = 1
        m = 1
        global tipo
        global valor
        global fondo
        global valors
        global evento
        global nombre
        tipo=" "
        valor=" "
        fondo=" "
        valores=" "
        evento=" "
        nombre=" "
        while i < len(codigo):
            cade= codigo[i]
            #ESTADO 0
            if estado == 0:
                if cade == '<':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Signo_menor', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == '>':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Signo_mayor', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == '~':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Virgulilla', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == ',':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Coma', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == ':':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Dos_puntos', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == '-':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Guion', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == '[':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Corchete_Abrir', fila, columna))
                    buffer = ''
                    columna += 1
                elif cade == ']':
                    buffer += cade
                    self.listaTokens.append(tokens(buffer, 'Corchete_Cerrar', fila, columna))
                    buffer = ''
                    columna += 1
                elif re.search('\s*"[\w\s,\.]+"', cade):
                    buffer += cade
                    columna += 1
                    estado = 1
                elif cade=='"' or re.search('[a-zA-Z]',cade):
                    buffer += cade
                    columna += 1
                    estado = 4
                elif cade=="'" or re.search('[a-zA-Z]',cade):
                    buffer += cade
                    columna += 1
                    estado = 4
                elif cade == '\n':
                    fila += 1
                    columna = 1
                elif cade == '\t' or cade==' ':
                    columna += 1
                elif cade == centinela:
                    columna +=1
                    buffer += cade
                    if i == len(codigo):
                        print("Se analizo con exito el archivo")
                        self.listaTokens.append(tokens(buffer, '<<EOFF>>', fila, columna))
                    else: 
                        print("No se puedo analizar por completo")
                        self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    
                else:
                    buffer += cade
                    self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    columna += 1
            elif  estado == 1:
                if re.search('\s*"[\w\s,\.]+"', cade):
                    buffer += cade
                    columna += 1
                    estado = 1
                elif cade ==',':
                    buffer += cade
                    columna += 1
                    estado = 2
                else:
                    self.listaTokens.append(tokens(buffer, 'Cadena', fila, columna))
                    buffer = ''
                    i -=1
                    estado = 0
            elif  estado == 2:
                if re.search('\s*"[\w\s,\.]+"', cade):
                    buffer += cade
                    columna += 1
                    estado = 2
                else:
                    self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    i -=1
                    estado = 0
            elif  estado == 3:
                if re.search('\s*"[\w\s,\.]+"', cade):
                    self.listaTokens.append(tokens(buffer, 'Cadena', fila, columna))
                    buffer = ''
                    estado = 3
                    '''
                    tipo=re.findall(r'tipo\s*:\s*"[\w\s,\.]+"',cade,flags=re.I)
                    valor=re.findall(r'valor\s*:\s*"[\w\s,\.]+"',cade,flags=re.I)
                    fondo=re.findall(r'fondo\s*:\s*"[\w\s,\.]+"',cade,flags=re.I)
                    #   busacar expresion regular para listas, agregarlos como que si fuera una matriz
                    #valores=re.findall(r'valores\s*:\[\s*"[\w\s,\.]+"',cade,flags=re.I)
                    valores="['Masculino','Femenino']"
                    valores=valores.replace(' ','')
                    valores=valores.replace("'",'')
                    evento=re.findall(r'evento\s*:\s*"[\w\s,\.]+"',cade,flags=re.I)
                    nombre=re.findall(r'nombre\s*:\s*"[\w\s,\.]+"',cade,flags=re.I)
                    '''
                else: 
                    self.listaTokens.append(tokens(buffer, 'Cadena', fila, columna))
                    buffer = ''
                    estado = 0
            elif  estado == 4:
                if cade=='"' or re.search('[a-zA-Z]',cade) or re.search('\s*"[\w\s,\.]+"', cade):
                    buffer += cade
                    columna += 1
                    estado = 4
                else: 
                    tipotoken=""
                    if buffer.lower=="formulario":
                        tipotoken="FORMULARIO"
                    elif buffer.lower=="tipo":
                        tipotoken="TIPO"
                        tipo = ""
                        tmp = i+2
                        while cade[tmp] != '\"':
                            tipo += cade[tmp]
                            tmp += 1
                    elif buffer.lower=="valor":
                        tipotoken="VALOR"
                        valor = ""
                        tmp = i+1
                        while cade[tmp] != '\"':
                            valor += cade[tmp]
                            tmp += 1
                    elif buffer.lower=="fondo":
                        tipotoken="FONDO"
                        fondo = ""
                        tmp = i+1
                        while cade[tmp] != '\"':
                            fondo += cade[tmp]
                            tmp += 1
                    elif buffer.lower=="nombre":
                        tipotoken="NOMBRE"
                        nombre = ""
                        tmp = i+1
                        while cade[tmp] != '\"':
                            nombre += cade[tmp]
                            tmp += 1
                    elif buffer.lower=="valores":
                        tipotoken="VALORES"
                        valores = ""
                        tmp = i+1
                        while cade[tmp] != '\"':
                            valores += cade[tmp]
                            tmp += 1
                    elif buffer.lower=="evento":
                        tipotoken="EVENTO"
                        evento = ""
                        tmp = i+1
                        while cade[tmp] != '\"':
                            evento += cade[tmp]
                            tmp += 1
                    else: 
                        tipotoken="IDENTIFICADOR"
                    self.listaTokens.append(tokens(buffer, tipotoken, fila, columna))
                    self.listaHtml.append(html(tipotoken,valor.strip(),fondo.strip(),valores.strip(),evento.strip(),nombre.strip()))
                    buffer = ''
                    i -= 1
                    estado = 0
            i += 1
        return codigo
        '''
        while i < len(codigo):
            cade= codigo[i]
            #ESTADO 0
            if estado == 0:
                #signos
                if cade == ',':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Coma',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1        
                elif cade == ':':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens( 'Dos_puntos',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1 
                elif cade == '<':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Signo_menor',buffer, fila, columna))
                    buffer = ''                    
                    estado = 0
                    i+=1
                elif cade == '>':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Signo_mayor',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1
                elif cade == '~':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Virgulilla',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1
                elif cade == '-':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Guion',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1
                elif cade == '[':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Corchete_Abrir',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1
                elif cade == ']':
                    columna += 1
                    buffer += cade
                    self.listaTokens.append(tokens('Corchete_Cerrar',buffer, fila, columna))
                    buffer = ''
                    estado = 0
                    i+=1
                #palabras reservadas e identificadores
                elif re.search('[a-zA-Z]', cade):
                    columna += 1
                    buffer += cade
                    columna += 1
                    estado = 1 
                    i+=1
                #cadena
                elif cade == '"':
                    columna += 1
                    buffer += cade
                    estado = 2
                    i+=1
                #espacios, saltos de lineas, tabuladores
                elif cade == '\t' or cade==' ':
                    columna += 1
                    estado = 0
                    i+=1
                elif cade == '\n':
                    columna = 1
                    fila += 1
                    estado = 0
                    i+=1
                #centinela
                elif cade == centinela:
                    buffer += cade
                    if i == len(codigo)-1:
                        print("Se analizo con exito el archivo")
                        self.listaTokens.append(tokens('<<EOFF>>',buffer, fila, columna))
                    else: 
                        print("No se puedo analizar por completo")
                        self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    columna +=1
                    i+=1
                    estado = 0
                    break
                #errores
                else:
                    buffer += cade
                    self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    columna +=1
                    i+=1
                    estado = 0
            # ESTADO 1 -palabras reservadas
            elif estado == 1:
                if re.search('[a-zA-Z]', cade):
                    buffer += cade
                    columna +=1
                    estado = 1 
                    i+=1
                else:
                    global Palabrareservada
                    Palabrareservada=True
                    tipotoken=""
                    if buffer.lower()=="tipo":
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
                        Palabrareservada=False
                        tipotoken="IDENTIFICADOR"
                    if Palabrareservada==True:
                        if buffer.lower()=="formulario":
                            self.listaTokens.append(tokens(tipotoken,buffer, fila, columna))
                            buffer = ''
                            estado = 0
                        else:
                            self.listaTokens.append(tokens(tipotoken,buffer, fila, columna))
                            buffer = ''
                            estado = 0
                    else:
                        self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                        buffer = ''
                        i+=1
                        estado = 0
            # ESTADO 2-cadena
            elif estado == 2:
                if cade == '"':
                    self.listaTokens.append(tokens("Cadena",buffer, fila, columna))
                    buffer = ''
                    columna += 1
                    i+=1
                    estado = 0
                else:
                    buffer += cade
                    columna = 1
                    estado =2
                    i+=1
            i += 1
        '''
    def imprimir(self):
        print("\n\n==========Lista tokens===============")
        for i in self.listaTokens:
            i.strToken()

        print("\n\n==========Lista errores===============")
        for o in self.listaErrores:
            o.strError()

        print("PROBANDO HTML")
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
        #etiqueta- <label>
        #texto- <input type="text" name="tipo_de_dato"/>
        # grupo-radop-  <input type="radio" name="empleoactual" value="tiempocompleto"> 
        #grupo-option - <select name="select">
            #<option value="value1">Value 1</option>
            #<option value="value2" selected>Value 2</option>
            #<option value="value3">Value 3</option>
        #</select>
        #boton- <input type="button">
        #
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Formulario</title>
                <meta charset="utf-8">
                <meta name="html" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	            </head>
                <body>"""
        for f in range(0,len(self.listaHtml)):
            if(self.listaHtml[f-1].tipo=="etiqueta"):
                texto1 = texto1 + "<label>"+self.listaHtml[f-1].valor+"</label><br>"
            if(self.listaHtml[f-1].tipo=="texto"):
                texto1 = texto1 + " <input type=\"text\" id=\""+self.listaHtml[f-1].valor+"\"placeholder=\""+self.listaHtml[f-1].fondo+"\"/><br>"
            if(self.listaHtml[f-1].tipo=="grupo-radio"):
                for u in range(0,len(valoress)):
                    texto1 = texto1 + "<input type=\"radio\"  value=\""+self.listaHtml[f-1].valor+"\">"+valoress[u-1].valor+"<br><br>"
            if(self.listaHtml[f-1].tipo=="grupo-radio"):
                for o in range(0,len(valoress)):
                    texto1 = texto1 + "<select name=\"select\"><option>"+valoress[o-1].valor+"</option></select><br>"
            if(self.listaHtml[f-1].tipo=="boton"):
                texto1 = texto1 + "<input type=\"button\"  value=\""+self.listaHtml[f-1].valor+"\"placeholder=\""+self.listaHtml[f-1].fondo+"\"/><br>"
                if(self.listaHtml[f-1].evento=="entrada"):
                    texto1 = texto1 + "<iframe width=\"500px\" height=\"500px\">"
        texto1= texto1+"""</body>
                         </html>
                        """
        doc = open('Formulario.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab('Formulario.html')