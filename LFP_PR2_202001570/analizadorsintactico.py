from ast import Lambda
from tokens import tokens
from error import error
import re
import webbrowser
from analizadorlexico import analizadorlexico
from partidopuntos import partidopuntos
class analizadorsintactico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.listaPartidos = []
        self.i=0
        self.resultado = []
        self.Jornada = []
        self.Parti = []
        self.PartiObt = []
        self.PartiObt1 = []
        self.PartiObt2 = []

    def analizar(self, listaTokens, listaErrores, listaPartidos, resultado):
        self.listaTokens= listaTokens
        self.listaErrores= listaErrores
        self.listaPartidos = listaPartidos
        self.resultado = resultado
        self.i=0
        self.Jornada = []
        self.Parti = []
        self.PartiObt = []
        self.PartiObt1 = []
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
                                                    self.buscarpartido(cadena,cadena1,primerano,segunano)                                                   
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
                                        self.BuscJornada(numero,primerano,segunano,docu)
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
                archivo="jornada"
                return archivo
        else:
            archivo="jornada"
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
                equipo= token.lexema
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
                                    self.Goles(condicion,equipo,primerano,segunano)      
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
                                    self.resultado.append("Generando archivo de clasificación de temporada "+primerano+"-"+segunano)
                                    self.Agregar(primerano,segunano)
                                    self.HTMLTABLA(docu)
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
                archivo="temporada"
                return archivo
        else:
            archivo="temporada"
            return archivo
        
    def temporadaequipo(self):
        token = self.listaTokens[self.i]
        if len(self.listaTokens)<8:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
        elif token.tipo == 'PARTIDOS':
            self.i += 1
            token = self.listaTokens[self.i]
            if token.tipo == 'Cadena':
                parti=token.lexema
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
                                                tempo="No"
                                                print(tempo)
                                                if len(self.listaTokens)>=12:
                                                    self.i +=1
                                                    token=self.listaTokens[self.i]
                                                    if token.tipo == '-ji':
                                                        tempo=self.archivop1()
                                                        print(tempo)
                                                    else: 
                                                        self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                                            elif token.tipo == '-ji':
                                                tempo=self.archivop1()
                                                print(tempo)
                                                docu="partidos"
                                                print(docu)
                                            else: 
                                                docu="partidos"
                                                tempo="No"
                                                print(docu)
                                                print(tempo)
                                            self.ObPartidos(parti,primerano,segunano,docu,tempo)
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
                    var=str(num1)+","+str(num2)
                    return var
                else:
                    #Se esperaba numero
                    self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                    return "No"
            else:
                #Se esperaba -jf
                self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
                return "No"
        else:
            #Se esperaba numero
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))
            return "No"
            
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
                                    self.Agregar(primerano,segunano)
                                    self.TOP(condicion,docu)
                                    prueba="\n"
                                    for recu in self.PartiObt2:
                                        prueba=prueba+"Partido: "+recu.partido+" Punteo: "+str(recu.puntos)+"\n"
                                    self.resultado.append("El top "+condicion.lower()+" de la temporada "+primerano+"-"+segunano+" fue: " +prueba)
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
            self.resultado.append("ADIOS")
        else:
            self.listaErrores.append(error('Error Sintactico', token.lexema, token.fila, token.columna))

    def buscarpartido(self, local, visitante, anioinicio, aniofin):
        temporada = str(anioinicio) + '-' + str(aniofin)
        for partido in self.listaPartidos:
            if partido['Temporada'] == temporada:
                if(partido['Equipo1'] == local and partido['Equipo2'] == visitante):
                    self.resultado.append("El resultado de este partido fue: "+ partido['Equipo1']+" " +partido['Goles1']+'-'+partido['Equipo2']+" "+partido['Goles2'])                 
                else:
                    pass
            else:
                pass
    
    def BuscJornada(self,numero,primerano,segunano,docu):
        temporada = str(primerano) + '-' + str(segunano)
        for partido in self.listaPartidos:
            if partido['Temporada'] == temporada:
                if partido['Jornada'] == numero:                   
                    self.resultado.append("Generando archivo de resultados jornada "+partido['Jornada']+" temporada "+ partido['Temporada'])
                    self.Jornada.append(partido)
                else:
                    pass
            else:
                pass
        if len(self.Jornada)>0:
            self.HTMLJORNADA(docu)

    def ObPartidos(self,parti,primerano,segunano,docu,tempo):
        temporada = str(primerano) + '-' + str(segunano)
        for partido in self.listaPartidos:
            if partido['Temporada'] == temporada:
                if partido['Equipo1'] == parti or partido['Equipo2'] == parti:
                    if tempo=="No":
                        self.Parti.append(partido)
                        self.resultado.append("Generando archivo de resultados de temporada "+partido['Temporada']+" del "+ parti)
                    else:
                        datos=tempo.split(",")
                        if int(partido['Jornada'])>=int(datos[0]) and int(partido['Jornada'])<=int(datos[1]):
                            self.Parti.append(partido)
                            self.resultado.append("Generando archivo de resultados de temporada "+partido['Temporada']+" del "+ parti)
                        else:
                            print("Error")

        if len(self.Parti)>0:
            self.HTMLPARTI(docu)

    def Goles(self,condicion,equipo,primerano,segunano):
        global contador1
        contador1=0
        temporada = str(primerano) + '-' + str(segunano)
        for partido in self.listaPartidos:
            if partido['Temporada'] == temporada:
                if condicion=="LOCAL":
                    if partido['Equipo1'] == equipo:
                        contador1 = contador1+int(partido['Goles1'])
                    else:
                        pass
                elif condicion=="VISITANTE":
                    if partido['Equipo2'] == equipo:
                        contador1 = contador1+int(partido['Goles2'])
                    else:
                         pass
                elif condicion=="TOTAL":
                    if partido['Equipo1'] == equipo:
                        contador1 = contador1+int(partido['Goles1'])
                    else:
                         pass
                    if partido['Equipo2'] == equipo:
                        contador1 = contador1+int(partido['Goles2'])
                    else:
                         pass
                else: 
                     pass
            else: 
                     pass
        print(contador1)
        self.resultado.append("Los goles anotados por el "+equipo+" en total en la temporada "+ temporada +" fueron "+str(contador1))
    
    def TOP(self,condicion,docu):
        contador=0
        self.PartiObt1.sort(key=lambda x:x.puntos)
        if condicion=="SUPERIOR":
            for reco in range(len(self.PartiObt1)):
                contador +=1
            inicio=contador-int(docu)
            for reco in range(inicio,contador):
                self.PartiObt2.append(self.PartiObt1[reco-1])
        elif condicion=="INFERIOR":
            for reco in range(0,int(docu)):
                self.PartiObt2.append(self.PartiObt1[reco])
        else:
            pass
        print(self.PartiObt2)

    def Agregar(self,primerano,segunano):
        viendo = []
        dic = []
        temporada = str(primerano) + '-' + str(segunano)
        for partido in self.listaPartidos:
            if partido['Temporada'] == temporada:
                viendo.append(partido["Equipo1"])
                viendo.append(partido["Equipo2"])
                dic.append(partido)
            else: 
                pass
        viendo=list(set(viendo))  
        puntoseq1=0
        puntoseq2=0     
        for partido in dic:
            for ver in viendo:
                if partido['Equipo1'] == ver:
                    if  partido ['Goles1'] >  partido [ 'Goles2' ]:
                        self.PartiObt.append(partidopuntos ( partido [ 'Equipo1' ], int ( 3 )))
                    elif  partido [ 'Goles1' ] == partido [ 'Goles2' ]:
                        self.PartiObt.append(partidopuntos ( partido [ 'Equipo1' ], int ( 1 )))
                    else :
                        self.PartiObt.append(partidopuntos ( partido [ 'Equipo1' ], int ( 0 )))
                elif  partido [ 'Equipo2' ] ==  ver :
                    if  partido [ 'Goles1' ] <  partido [ 'Goles2' ]:
                        self.PartiObt.append ( partidopuntos ( partido [ 'Equipo2' ], int ( 3 )))
                    elif  partido [ 'Goles1' ] == partido [ 'Goles2' ]:
                        self.PartiObt.append ( partidopuntos ( partido [ 'Equipo2' ], int ( 1 )))
                    else :
                        self.PartiObt.append ( partidopuntos ( partido [ 'Equipo2' ], int ( 0 )))
        global diccionario_partido
        diccionario_partido={}
        for recorriendo in self.PartiObt:
            if recorriendo.partido in diccionario_partido:
                punto_anterior=diccionario_partido[recorriendo.partido]
                punto_nuevo=punto_anterior+recorriendo.puntos
                diccionario_partido[recorriendo.partido]=punto_nuevo
            else:
                diccionario_partido[recorriendo.partido]=recorriendo.puntos
        lista_keys=list(diccionario_partido.keys())
        lista_values=list(diccionario_partido.values())
        for i in range(len(lista_keys)):
            self.PartiObt1.append(partidopuntos(lista_keys[i],lista_values[i]))

    def HTMLJORNADA(self,docu):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Reporte de Jornadas</title>
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
					            <h2 class="heading-section">Tabla de Partidos</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Fecha</th>
						                <th>Temporada</th>
						                <th>Jornada</th>
						                <th>Equipo1</th>
                                        <th>Equipo2</th>
                                        <th>Goles1</th>
                                        <th>Goles2</th>
						                </tr>
						            </thead>"""
        for jornada in self.Jornada:
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+str(jornada['Fecha'])+"</center></td><td><center>"+str(jornada['Temporada'])+"</center></td><td><center>"+str(jornada['Jornada'])+"</center></td><td><center>"+str(jornada['Equipo1'])+"</center></td><td><center>"+str(jornada['Equipo2'])+"</center></td><td><center>"+str(jornada['Goles1'])+"</center></td><td><center>"+str(jornada['Goles2'])+"</center></td></tr>"
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
        doc = open(docu+'.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab(docu+'.html')

    def HTMLPARTI(self,docu):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Temporada de un equipo</title>
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
					            <h2 class="heading-section">Temporada de un equipo</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Fecha</th>
						                <th>Temporada</th>
						                <th>Jornada</th>
						                <th>Equipo1</th>
                                        <th>Equipo2</th>
                                        <th>Goles1</th>
                                        <th>Goles2</th>
						                </tr>
						            </thead>"""
        for jornada in self.Parti:
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+str(jornada['Fecha'])+"</center></td><td><center>"+str(jornada['Temporada'])+"</center></td><td><center>"+str(jornada['Jornada'])+"</center></td><td><center>"+str(jornada['Equipo1'])+"</center></td><td><center>"+str(jornada['Equipo2'])+"</center></td><td><center>"+str(jornada['Goles1'])+"</center></td><td><center>"+str(jornada['Goles2'])+"</center></td></tr>"
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
        doc = open(docu+'.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab(docu+'.html')
    
    def listavacia(self,lista):
        return not lista

    def HTMLTABLA(self,docu):
        texto1 = """<!doctype html>
                <html lang="en">
                <head>
  	            <title>Tabla temporada</title>
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
					            <h2 class="heading-section">Tabla Temporada</h2>
				            </div>
			            </div>
			        <div class="row">
				        <div class="col-md-12">
					        <div class="table-wrap">
						        <table class="table table-dark">
						            <thead>
						                <tr class="bg-dark">
						                <th>Equipo</th>
                                        <th>Puntos</th>
						                </tr>
						            </thead>"""
        for jornada in self.PartiObt1:
            texto1 = texto1 + "<tr class=\"bg-primary\"><td><center>"+str(jornada.partido)+"</center></td><td><center>"+str(jornada.puntos)+"</center></td></tr>"
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
        doc = open(docu+'.html','wb')
        doc.write(bytes(texto1,"'utf-8'"))
        doc.close()
        webbrowser.open_new_tab(docu+'.html')