from tablaSimbolos.Tipo import tipos

class tablaSimbolos:
    def __init__(self, anterior = None):
        self.anterior = anterior
        self.tabla = {}
        self.tipo = tipos.ENTERO
        self.entorno = ""
    
    def setVariable(self, simbolo):
        if simbolo.id in self.tabla:
            return Exception("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.row, simbolo.column)
        self.tabla[simbolo.id] = simbolo
        return None        
    
    def getVariable(self, id):
        tmp = self
        while(tmp != None):
            if id in tmp.tabla:
                return tmp.tabla[id]
            tmp = tmp.getAnterior()
        return None
    
    def updateVariable(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla :
                tablaActual.tabla[simbolo.id].setValue(simbolo.getValue())
                return None             # simbolo actualizado
            else:
                tablaActual = tablaActual.anterior
        
        self.tabla[simbolo.id] = simbolo
        return None # --> simbolo agregado
        
    def getTable(self):
        return self.tabla
    
    def setTable(self, table):
        self.tabla = table
    
    def getAnterior(self):
        return self.anterior
    
    def setAnterior(self, ant):
        self.anterior = ant
    
    def getEntorno(self):
        return self.entorno
    
    def setEntorno(self, entorno):
        self.entorno = entorno