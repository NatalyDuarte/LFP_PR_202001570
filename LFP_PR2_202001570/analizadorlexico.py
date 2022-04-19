from tokens import tokens
from error import error
import re
class analizadorr:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        #self.listaHtml = []

    def limpiartokens(self):
        self.listaTokens = []

    def limpiartokens(self):
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
                if cade == ">":
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
                elif cade == "-":
                    columna+=1
                    buffer+=cade
                    self.listaTokens.append(tokens('Guion',buffer, fila, columna))
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
                elif re.search('-[\w\s,\.]+',cade):
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
                #fechas 
                elif re.search('\s*<[0-9-]+>',cade):
                    columna+=1
                    buffer+= cade
                    estado=4
                    i+=1
                #instruccion
                elif re.search('[\w\s,\.]+',cade):
                    columna+=1
                    buffer+= cade
                    estado=5
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
                    columna+=1
                    self.listaErrores.append(error('Error Léxico', cade, fila, columna))
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
                else:
                    buffer+=cade
                    columna+=1
                    estado=2
                    i+=1
            #Numeros
            elif estado == 3:
                if re.search('[0-9]',cade):
                    buffer = buffer.replace("\"","")
                    self.listaTokens.append(tokens('Número',buffer, fila, columna))
                    estado=0
                    buffer=''
                    i+=1
                else:
                    buffer+=cade
                    columna+=1
                    estado=3
                    i+=1
            #Fechas
            elif estado == 4:
                if re.search('\s*<[0-9-]+>',cade):
                    buffer = buffer.replace("\"","")
                    self.listaTokens.append(tokens('Fecha',buffer, fila, columna))
                    estado=0
                    buffer=''
                    i+=1
                else:
                    buffer+=cade
                    columna+=1
                    estado=4
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