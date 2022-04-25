from tokens import tokens
from error import error
import re
class analizadorlexico:
    def __init__(self):
        pass

    def analizar(self, codigo, listaTokens, listaErrores):
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
                    listaTokens.append(tokens('Corchete_Abrir',buffer, fila, columna))
                    buffer=""  
                    estado=0
                    i+=1               
                if cade == ">":
                    columna+=1
                    buffer+=cade
                    listaTokens.append(tokens('Signo_mayor',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1      
                elif cade == "<":
                    columna+=1
                    buffer+=cade
                    listaTokens.append(tokens('Signo_menor',buffer, fila, columna))
                    buffer=""
                    estado=0
                    i+=1                     
                elif cade == "]":
                    columna+=1
                    buffer+= cade
                    listaTokens.append(tokens('Corchete_Cerrar',buffer, fila, columna))
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
                elif re.search('[A-Za-z0-9_]',cade):
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
                    listaErrores.append(error('Error Léxico', cade, fila, columna))
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
                    #columna=columna-1
                    listaTokens.append(tokens(tipotoken,buffer, fila, columna))
                    buffer = ''
                    estado=0  
            #Cadenas                 
            elif estado == 2:
                if cade == '"':
                    buffer = buffer.replace("\"","")
                    listaTokens.append(tokens('Cadena',buffer, fila, columna))
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
                        listaTokens.append(tokens('Fecha',buffer, fila, columna))
                    elif re.search(r'\d\d',buffer):
                        listaTokens.append(tokens('Número',buffer, fila, columna))
                    elif re.search(r'\d',buffer):
                        listaTokens.append(tokens('Número',buffer, fila, columna))
                    else:
                        listaTokens.append(tokens('Número',buffer, fila, columna))                  
                    buffer=''
                    estado=0
            #Instruccion
            elif estado == 4:
                if re.search('[A-Za-z0-9_]',cade):
                    buffer+=cade
                    columna+=1
                    estado=4
                    i+=1 
                else:
                    listaTokens.append(tokens('Archivo',buffer, fila, columna))
                    estado=0
                    buffer=''
                    i+=1