from tokens import tokens
from error import error
import re
import webbrowser
from analizadorlexico import analizadorlexico
class analizadorsintactico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.i=0

    def analizar(self, listaTokens, listaErrores):
        self.listaTokens= listaTokens
        self.listaErrores= listaErrores
        self.inicio()

    def inicio(self):
        token= self.listaTokens[self.i]
        self.lista_instru()
        token = self.listaTokens[self.i]
        if token.tipo =="<EOF>":
            print("Analisis sintactico exitoso")

    def lista_instru(self):
        global token
        token= self.listaTokens[self.i]
        tipo=token.tipo
        if tipo=="RESULTADO" or tipo=="JORNADA" or tipo=="GOLES" or tipo=="TABLA" or tipo=="PARTIDOS" or tipo=="TOP" or tipo=="ADIOS" :
            self.instruccion()
            #self.lista_instru()
        elif tipo=="<EOF>":
            return
        else:
            #Error
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        
    def instruccion(self):
        token = self.listaTokens[self.i]
        tipo = token.tipo
        if tipo == 'RESULTADO':
            self.resultadopartido()
        elif tipo == 'JORNADA':
            self.resultadojornada()
        elif tipo == 'GOLES':
            self.totalgolestemporada()
        elif tipo == 'TABLA':
            self.tablageneraltemporada()
        elif tipo == 'PARTIDOS':
            self.temporadaequipo()
        elif tipo == 'TOP':
            self.topequipos()
        elif tipo == 'ADIOS':
            self.adios()
            
    def resultadopartido(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<10:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'RESULTADO':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'Cadena':
                    cadena = token.lexema
                    self.i += 1
                    token = self.listaTokens[self.i]
                    if token.tipo == 'VS':
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Cadena':
                            cadena1 = token.lexema
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'TEMPORADA':
                                self.i += 1
                                token = self.listaTokens[self.i]                            
                                if token.tipo == 'Signo_menor':
                                    self.i += 1
                                    token = self.listaTokens[self.i]
                                    if token.tipo == 'Fecha':
                                        primerano= token.lexema
                                        self.i += 1
                                        token = self.listaTokens[self.i]
                                        if token.tipo == 'Guion':
                                            self.i += 1
                                            token = self.listaTokens[self.i]
                                            if token.tipo == 'Fecha':
                                                segunano= token.lexema
                                                self.i += 1
                                                token = self.listaTokens[self.i]        
                                                if token.tipo == 'Signo_mayor':
                                                    print("Todo correcto")
                                                else:
                                                    #Se esperaba signo mayor
                                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                            else:
                                                #Se esperaba fecha
                                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                        else:
                                            #se esperaba guion 
                                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                    else:
                                        #se esperaba fecha 
                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                else:
                                    #se esperaba signo menor 
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #se esperaba temporada 
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                        else:
                            #se esperaba cadena 
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    else:
                        #se esperaba vs
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                else:
                    #se esperaba cadena 
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        else:
            #se esperaba resultado 
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
    
    def resultadojornada(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<8:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'JORNADA':
            self.i += 1
            token = self.listaTokens[self.i]
            if token.tipo == 'Número':
                numero = token.lexema
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.listaTokens[self.i]                            
                    if token.tipo == 'Signo_menor':
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Fecha':
                            primerano= token.lexema
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'Guion':
                                self.i += 1
                                token = self.listaTokens[self.i]
                                if token.tipo == 'Fecha':
                                    segunano= token.lexema
                                    self.i += 1
                                    token = self.listaTokens[self.i]        
                                    if token.tipo == 'Signo_mayor':
                                        print("Todo correcto")
                                        docu=self.archivoop()
                                        print(docu)
                                    else:
                                        #Se esperaba signo mayor
                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                else:
                                    #Se esperaba Fecha
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #Se esperaba guion
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                        else:
                            #Se esperaba fecha
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    else:
                        #Se esperaba signo menor
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))   
                else:
                    #Se esperaba temporada
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))  
            else:
                #Se esperaba numero
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))          
        else:
            #se esperaba jornada
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))

    def archivoop(self):
        if len(self.listaTokens)>=9:
            self.i+=1
            token=self.listaTokens[self.i]
            if token.tipo == '-f':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'Archivo':
                    nombre= token.lexema
                    return nombre
                else:
                    #Se esperaba archivo
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            else:
                archivo="jornada.html"
                return archivo
        else:
            archivo="jornada.html"
            return archivo
                
    def totalgolestemporada(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<9:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'GOLES':
            self.i += 1
            condicion= self.condicion()
            token = self.listaTokens[self.i]
            if token.tipo == 'Cadena':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.listaTokens[self.i]                            
                    if token.tipo == 'Signo_menor':
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Fecha':
                            primerano= token.lexema
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'Guion':
                                self.i += 1
                                token = self.listaTokens[self.i]
                                if token.tipo == 'Fecha':
                                    segunano= token.lexema                                    
                                    self.i += 1
                                    token = self.listaTokens[self.i]        
                                    if token.tipo == 'Signo_mayor':
                                        print("Todo correcto")
                                    else:
                                        #Se esperaba signo mayor
                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                else:
                                    #Se esperaba Fecha
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #Se esperaba guion
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))                        
                        else:
                            #Se esperaba fecha
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    else:
                        #Se esperaba signo menor
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))   
                else:
                    #Se esperaba temporada
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna)) 
            else:
                #Se esperaba cadena
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna)) 
        else:
            #Se esperaba goles
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))  

    def condicion(self):
        token = self.listaTokens[self.i]
        if token.tipo == 'LOCAL':
            self.i += 1
            return token.lexema
        elif token.tipo == 'VISITANTE':
            self.i += 1
            return token.lexema
        if token.tipo == 'TOTAL':
            self.i += 1
            return token.lexema
        else:
            # error 
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            return '<<error>>'

    def tablageneraltemporada(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<7:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'TABLA':
            self.i += 1
            token = self.listaTokens[self.i]
            if token.tipo == 'TEMPORADA':
                self.i += 1
                token = self.listaTokens[self.i]                            
                if token.tipo == 'Signo_menor':
                    self.i += 1
                    token = self.listaTokens[self.i]
                    if token.tipo == 'Fecha':
                        primerano= token.lexema
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Guion':
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'Fecha':
                                segunano= token.lexema                                    
                                self.i += 1
                                token = self.listaTokens[self.i]        
                                if token.tipo == 'Signo_mayor':
                                    print("Todo correcto")
                                    docu=self.archivoopp()
                                    print(docu)
                                else:
                                    #Se esperaba signo mayor
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #Se esperaba Fecha
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                        else:
                            #Se esperaba guion
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))                        
                    else:
                        #Se esperaba fecha
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                else:
                    #Se esperaba signo menor
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))   
            else:
                #Se esperaba temporada
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        else:
            #Se esperaba tabla
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna)) 

    def archivoopp(self):
        if len(self.listaTokens)>=9:
            self.i+=1
            token=self.listaTokens[self.i]
            if token.tipo == '-f':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'Archivo':
                    nombre= token.lexema
                    return nombre
                else:
                    #Se esperaba archivo
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            else:
                archivo="temporada.html"
                return archivo
        else:
            archivo="temporada.html"
            return archivo
        
    def temporadaequipo(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<8:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'PARTIDOS':
            self.i += 1
            token = self.listaTokens[self.i]
            if token.tipo == 'Cadena':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.listaTokens[self.i]                            
                    if token.tipo == 'Signo_menor':
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Fecha':
                            primerano= token.lexema
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'Guion':
                                self.i += 1
                                token = self.listaTokens[self.i]
                                if token.tipo == 'Fecha':
                                    segunano= token.lexema                                    
                                    self.i += 1
                                    token = self.listaTokens[self.i]        
                                    if token.tipo == 'Signo_mayor':
                                        print("Todo correcto")
                                        if len(self.listaTokens)>=9:
                                            self.i+=1
                                            token=self.listaTokens[self.i]
                                            if token.tipo == '-f':
                                                docu=self.archivoopp1()
                                                print(docu)
                                                if len(self.listaTokens)>=11:
                                                    self.i +=1
                                                    token=self.listaTokens[self.i]
                                                    if token.tipo == '-ji':
                                                        tempo=self.archivop1()
                                                        print(tempo)
                                                    else: 
                                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                            else:
                                                docu="partidos.html"
                                                print(docu)
                                            if token.tipo == '-ji':
                                                tempo=self.archivop1()
                                                print(tempo)
                                            else: 
                                                tempo="100"
                                                print(tempo)
                                        else:
                                            pass
                                    else:
                                        #Se esperaba signo mayor
                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                else:
                                    #Se esperaba Fecha
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #Se esperaba guion
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))                        
                        else:
                            #Se esperaba fecha
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    else:
                        #Se esperaba signo menor
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))   
                else:
                    #Se esperaba temporada
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            else:
                #Se esperaba cadena
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        else:
            #Se esperaba partidos
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))

    def archivoopp1(self):
        self.i += 1
        token = self.listaTokens[self.i]
        if token.tipo == 'Archivo':
            nombre= token.lexema
            return nombre
        else:
            #Se esperaba archivo
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
    
    def archivop1(self):
        self.i += 1
        token = self.listaTokens[self.i]
        if token.tipo == 'Número':
            num1= token.lexema
            self.i += 1
            token = self.listaTokens[self.i]
            if token.tipo == '-jf':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'Número':
                    num2= token.lexema
                    return str(num1),str(num2)
                else:
                    #Se esperaba numero
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    return "100"
            else:
                #Se esperaba -jf
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                return "100"
        else:
            #Se esperaba numero
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            return "100"
            

    def topequipos(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<8:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'TOP':
            self.i += 1
            condicion= self.condicion1()
            token = self.listaTokens[self.i]
            if token.tipo == 'TEMPORADA':
                self.i += 1
                token = self.listaTokens[self.i]                            
                if token.tipo == 'Signo_menor':
                    self.i += 1
                    token = self.listaTokens[self.i]
                    if token.tipo == 'Fecha':
                        primerano= token.lexema
                        self.i += 1
                        token = self.listaTokens[self.i]
                        if token.tipo == 'Guion':
                            self.i += 1
                            token = self.listaTokens[self.i]
                            if token.tipo == 'Fecha':
                                segunano= token.lexema                                    
                                self.i += 1
                                token = self.listaTokens[self.i]        
                                if token.tipo == 'Signo_mayor':
                                    print("Todo correcto")
                                    docu=self.archivop2()
                                    print(docu)
                                else:
                                    #Se esperaba signo mayor
                                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                            else:
                                #Se esperaba Fecha
                                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                        else:
                            #Se esperaba guion
                            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))                        
                    else:
                        #Se esperaba fecha
                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                else:
                    #Se esperaba signo menor
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))   
            else:
                #Se esperaba temporada
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        else:
            #Se esperaba top
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))

    def condicion1(self):
        token = self.listaTokens[self.i]
        if token.tipo == 'SUPERIOR':
            self.i += 1
            return token.lexema
        elif token.tipo == 'INFERIOR':
            self.i += 1
            return token.lexema
        else:
            # error 
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            return '<<error>>'
    def archivop2(self):
        if len(self.listaTokens)>=9:
            self.i+=1
            token=self.listaTokens[self.i]
            if token.tipo == '-n':
                self.i += 1
                token = self.listaTokens[self.i]
                if token.tipo == 'Número':
                    nombre= token.lexema
                    return nombre
                else:
                    #Se esperaba numero
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            else:
                archivo="5"
                return archivo
        else:
            archivo="5"
            return archivo
    
    def adios(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<1:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'ADIOS':
            print("Leido correctamente")
        else:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))