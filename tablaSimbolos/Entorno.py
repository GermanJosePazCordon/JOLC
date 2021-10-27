from tablaSimbolos.Simbolo import Simbolo

class Entorno:
    def __init__(self, last):
        self.last = last
        # NUEVO
        self.size = 0
        self.breakk = ''
        self.continuee = ''
        self.returnn = ''
        self.inFun = False
        if(last != None):
            self.size = last.size
            self.breakk = last.breakk
            self.continuee = last.continuee
            self.returnn = last.returnn
            self.inFun = last.inFun
        self.variables = {}
        self.functions = {}
        self.structs = {}
        
        
    def setVariable(self, ids, tipo, heap, vector):
        if ids in self.variables.keys():
            print("Ya existe la variable")
        else:
            variable = Simbolo(ids, tipo, self.size, self.last == None, heap, "", vector)
            self.size += 1
            self.variables[ids] = variable
        return self.variables[ids]

    def setFuncion(self, ids, funcion):
        if ids in self.functions.keys():
            print("Ya existe la funcion")
        else:
            self.functions[ids] = funcion
    
    def setStruct(self, ids, atributo):
        if ids in self.structs.keys():
            print("Ya existe el struct")
        else:
            self.structs[ids] = atributo

    def getVariable(self, varible):
        entorno = self
        while entorno != None:
            if varible in entorno.variables.keys():
                return entorno.variables[varible]
            entorno = entorno.last
        return None
    
    def getFuncion(self, funcion):
        entorno = self
        while entorno != None:
            if funcion in entorno.functions.keys():
                return entorno.functions[funcion]
            entorno = entorno.last
        return None
        
    def getStruct(self, struct):
        entorno = self
        while entorno != None:
            if struct in entorno.structs.keys():
                return entorno.structs[struct]
            entorno = entorno.last
        return None

    def getGlobal(self):
        entorno = self
        while entorno.last != None:
            entorno = entorno.last
        return entorno