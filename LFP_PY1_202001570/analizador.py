from tokens import tokens
from error import error
from html import html
import re
import webbrowser

class analizador:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []

    def analizar(self, codigo):
        self.listaTokens = []
        self.listaErrores = []
        self.listaHtml = []
        self.listaHtml.append(html("etiqueta","nombre","Ingrese nombre"," "," "," "))
        # VARIABLES
        fila = 1
        columna = 1
        buffer = ''
        centinela = '$'
        codigo += centinela
        estado = 0
        # AUTOMATA
        i = 0
        n = 0
        global tipo
        global valor
        global fondo
        global valores
        global evento
        global nombre
        global data
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
                    estado = 2 
                    i+=1
                #cadena
                elif cade == '\'' or cade == '"':
                    buffer += cade
                    columna += 1
                    estado = 1
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
                elif cade == '\r':
                    pass
                #centinela
                elif cade == centinela:
                    self.listaTokens.append(tokens('<<EOFF>>',buffer, fila, columna))
                    print('¡DATOS ACEPTADOS!')
                    break
                else:
                    buffer += cade
                    self.listaErrores.append(error('Error Léxico', buffer, fila, columna))
                    buffer = ''
                    columna += 1
                    i+=1
                    estado = 0       
           #ESTADO 1 - CADENA
            elif estado == 1:
                if cade == '\'' or cade == '"':
                    buffer += cade
                    self.listaTokens.append(tokens('Cadena',buffer, fila, columna))
                    buffer = ''
                    columna += 1
                    estado = 0
                elif cade == '\n':
                    buffer += cade
                    fila += 1
                    columna = 1
                elif cade == '\r':
                    buffer += cade
                else:
                    buffer += cade
                    columna += 1
           #ESTADO 2- LETRAS PALABRAS RESERVADAS
            elif estado == 3:
                if re.search('[A-Z]', cade):
                    buffer += cade
                    columna += 1
                else:
                    if buffer.lower() == 'tipo':
                        columna = columna-1
                        tipo = ""
                        tmp = i+2
                        while codigo[tmp] != '\"':
                            tipo += codigo[tmp]
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Tipo',buffer, fila, columna))
                        columna = columna+1
                    elif buffer.lower() == 'valor':
                        columna = columna-1
                        valor = ""
                        tmp = i+1
                        while codigo[tmp] != '\"':
                            valor += codigo[tmp]
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Valor',buffer, fila, columna))
                        columna = columna+1
                    elif buffer.lower() == 'fondo':
                        columna = columna-1
                        fondo = ""
                        tmp = i+1
                        while codigo[tmp] != '\"':
                            fondo += codigo[tmp]
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Fondo',buffer, fila, columna))
                        columna = columna+1
                    elif buffer.lower() == 'nombre':
                        columna = columna-1
                        nombre = ""
                        tmp = i+1
                        while codigo[tmp] != '\"':
                            nombre += codigo[tmp]
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Nombre',buffer, fila, columna))
                        columna = columna+1
                    elif buffer.lower()  == 'evento':
                        columna = columna-1
                        evento = ""
                        tmp = i+1
                        while codigo[tmp] != '\"':
                            evento += codigo[tmp]
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Evento',buffer, fila, columna))
                        columna = columna+1
                    elif buffer.lower() == 'valores':
                        valores = []
                        tmp = i+3
                        data = ''
                        while codigo[tmp] != "]":
                            if codigo[tmp] == "[":
                                tmp2 = tmp+1
                                while codigo[tmp2] != ']':
                                    data += codigo[tmp2]
                                    tmp2 += 1
                                data = data.replace("'"," ")
                                d = data.split(',')
                                valores.append(valores(d[0].strip(), d[1].strip(), d[2].strip()))
                                data = ''
                            tmp += 1
                        self.listaTokens.append(tokens('Palabra_Reservada_Valores',buffer, fila, columna))
                    elif buffer.lower() == 'formulario':
                        columna = columna-1
                        tmp = i+1
                        self.listaHtml.append(html(tipo.strip(), valor.strip(), fondo.strip(), nombre.strip(), evento.strip(), valores))
                        self.listaTokens.append(tokens('Palabra_Reservada_Formulario',buffer, fila, columna))
                        columna = columna+1
                    else:
                        self.listaErrores.append(error('Error Léxico',buffer, fila, columna))
                    buffer = ''
                    i -= 1
                    estado = 0
            i += 1
        return codigo
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
        pass