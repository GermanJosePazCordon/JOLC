from tablaSimbolos.Tipo import tipos
from abstract.NodoAST import NodoAST

class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.globall = ""
        self.errores = []
        self.listaTabla = []
        self.AST = ""
    
    def getInstruccion(self):
        return self.instrucciones
    
    def setInstruccion(self, instruccion):
        self.instrucciones = instruccion

    def getConsola(self):
        return self.consola

    def setConsola(self, consola):
        self.consola = consola
    
    def updateConsola(self, update):
        self.consola += str(update)
    
    def getGlobal(self):
        return self.globall

    def setGlobal(self, tabla):
        self.globall = tabla

    def addTabla(self, tabla):
        self.listaTabla.append(tabla)
    
    def getLista(self):
        return self.listaTabla

    def setLista(self, lista):
        self.listaTabla = lista
    
    def addError(self, err):
        self.errores.append(err)
    
    def getError(self):
        return self.errores
    
    def getRaiz(self, ast):
        nodo = NodoAST("RAIZ")
        nodo_instrs = NodoAST("INSTRUCCIONES")
        cont = 0
        for instruccion in ast.getInstruccion():
            if cont == 0:
                nodo_instr = NodoAST("INSTRUCCION")
                nodo_instr.agregarHijoNodo(instruccion.getNodo())
                nodo_instrs.agregarHijoNodo(nodo_instr)
            else:
                tmp = nodo_instrs
                nodo_instr = NodoAST("INSTRUCCION")
                nodo_instrs = NodoAST("INSTRUCCIONES")
                nodo_instrs.agregarHijoNodo(tmp)
                nodo_instr.agregarHijoNodo(instruccion.getNodo())
                nodo_instrs.agregarHijoNodo(nodo_instr)
            cont += 1        
        nodo.agregarHijoNodo(nodo_instrs)
        return nodo
    
    def getDot(self, raiz): ## DEVUELVE EL STRING DE LA GRAFICA EN GRAPHVIZ
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            nombreHijo = "n" + str(self.contador)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador += 1
            self.recorrerAST(nombreHijo, hijo)
    
    def getDotTable(self, tree):
        self.grafoTabla = ""
        self.grafoTabla += "digraph {\n"
        self.grafoTabla += "\nnode [color=black, fontname=" + '"' + "Segoe UI" + '"' + "]\n"
        self.grafoTabla += '"nombre"[shape=none, fontsize=10, margin=0, color=black, label=<\n'
        self.grafoTabla += '<TABLE  border="1">\n'
        self.grafoTabla +=  '<TR><TD><FONT FACE="Segoe UI">' + "Nombre" + '</FONT></TD>'
        self.grafoTabla += '<TD><FONT FACE="Segoe UI">' + "Tipo" + '</FONT></TD>'
        self.grafoTabla += '<TD><FONT FACE="Segoe UI">' + "Ambito" + '</FONT></TD>'
        self.grafoTabla += '<TD><FONT FACE="Segoe UI">' + "Fila" + '</FONT></TD>'
        self.grafoTabla += '<TD><FONT FACE="Segoe UI">' + "Columna" + '</FONT></TD></TR>\n'
        self.grafoTabla += self.recorrerTabla(tree)
        self.grafoTabla += '</TABLE>\n'
        self.grafoTabla += '>];\n'
        self.grafoTabla += "}"
        return self.grafoTabla
    
    def recorrerTabla(self, table):
        tablas = []
        tabla = []
        tablas.append(table)
        for i in table.tablas:
            tablas.append(i)
        
        for i in tablas:
            for key, value in table.variables.items():
                if i.entorno == '':
                    tabla.append(self.armarTupla(key, self.getTipo(value.tipo), "global", value.row, value.column))
                else:
                    tabla.append(self.armarTupla(key, self.getTipo(value.tipo), i.entorno, value.row, value.column))
            for key, value in table.functions.items():
                tabla.append(self.armarTupla(key, "Funcion", "global", value.line, value.column))
            for key, value in table.structs.items():
                tabla.append(self.armarTupla(key, "Struct", "global", value[3], value[4]))
        
        tablaSet = set(tabla)
        tmp = ""
        for i in tablaSet:
            tmp += str(i)
        return str(tmp)
    
    def getDotErr(self, tree):
        self.grafoErr = "";
        self.grafoErr += "digraph {\n"
        self.grafoErr += "\nnode [color=black, fontname=" + '"' + "Segoe UI" + '"' + "]\n"
        self.grafoErr += '"nombre"[shape=none, fontsize=10, margin=0, color=black, label=<\n'
        self.grafoErr += '<TABLE  border="1">\n'
        self.grafoErr +=  '<TR><TD><FONT FACE="Segoe UI">' + "No." + '</FONT></TD>'
        self.grafoErr += '<TD><FONT FACE="Segoe UI">' + "Descripcion" + '</FONT></TD>'
        self.grafoErr += '<TD><FONT FACE="Segoe UI">' + "Fila" + '</FONT></TD>'
        self.grafoErr += '<TD><FONT FACE="Segoe UI">' + "Columna" + '</FONT></TD>'
        self.grafoErr += '<TD><FONT FACE="Segoe UI">' + "Fecha y Hora" + '</FONT></TD></TR>\n'
        self.grafoErr += self.recorrerErr(tree)
        self.grafoErr += '</TABLE>\n';
        self.grafoErr += '>];\n'
        self.grafoErr += "}";
        return self.grafoErr;
        
    def recorrerErr(self, tree):
        tabla = []
        cont = 1
        for i in self.errores:
            tabla.append(self.armarTuplaErr(i.sms, i.row, i.column, i.date))
        tablaSet = set(tabla)
        tmp = ""
        for i in tablaSet:
            tmp += '<TR><TD><FONT FACE="Segoe UI">' + str(cont) + '</FONT></TD>' + str(i) +"\n"
            cont += 1;
        return str(tmp)
              
    def armarTupla(self, nombre, tipo, ambito, line, column):
        tupla = '<TR><TD><FONT FACE="Segoe UI">' + nombre + '</FONT></TD><TD><FONT FACE="Segoe UI">' + tipo + '</FONT></TD><TD><FONT FACE="Segoe UI">' + ambito + '</FONT></TD><TD><FONT FACE="Segoe UI">' + str(line) + '</FONT></TD><TD><FONT FACE="Segoe UI">' + str(column) + '</FONT></TD></TR>\n'
        return str(tupla)
    
    def armarTuplaErr(self, descripcion, line, column, time):
        tupla = '<TD><FONT FACE="Segoe UI">' + descripcion + '</FONT></TD><TD><FONT FACE="Segoe UI">' + str(line) + '</FONT></TD><TD><FONT FACE="Segoe UI">' + str(column) + '</FONT></TD><TD><FONT FACE="Segoe UI">' + str(time) + '</FONT></TD></TR>\n'
        return str(tupla)
    
    def getTipo(self, tipo):
        if tipo == tipos.ENTERO:
            return "Int64"
        elif tipo == tipos.DECIMAL:
            return "Float64"
        elif tipo == tipos.CADENA:
            return "String"
        elif tipo == tipos.CARACTER:
            return "Char"
        elif tipo == tipos.BOOLEAN:
            return "Bool"
        elif tipo == tipos.STRUCT:
            return "Struct"
        elif tipo == tipos.VECTOR:
            return "Array"
        elif tipo == tipos.NULO:
            return "Nothing"
        elif tipo == tipos.FUNCION:
            return "Funcion"

        