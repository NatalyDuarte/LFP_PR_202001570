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
                                            if len(self.listaTokens)>self.i and token.tipo == 'Fecha':
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
        pass

    def archivoop(self):
        pass

    def totalgolestemporada(self):
        pass

    def condicion(self):
        pass

    def tablageneraltemporada(self):
        pass

    def temporadaequipo(self):
        pass

    def archivop1(self):
        pass

    def topequipos(self):
        pass
    
    def archivop2(self):
        pass
    
    def adios(self):
        pass