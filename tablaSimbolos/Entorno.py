from tablaSimbolos.Simbolo import Simbolo

class Entorno:
    def __init__(self, last):
        self.last = last
        # NUEVO
        self.size = 0
        if(last != None):
            self.size = self.last.size
        self.variables = {}
        self.functions = {}
        self.structs = {}
    
    def saveVar(self, ids, tipo, heap):
        if ids in self.variables.keys():
            print("Ya existe la variable")
        else:
            variable = Symbol(ids, tipo, self.size, self.last == None, heap)
            self.size += 1
            self.variables[ids] = variable
        return self.variables[ids]

    def saveFunc(self, ids, funcion):
        if ids in self.functions.keys():
            print("Ya existe la funcion")
        else:
            self.functions[ids] = funcion
    
    def saveStruct(self, ids, atributo):
        if ids in self.structs.keys():
            print("Ya existe el struct")
        else:
            self.structs[ids] = atributo

    def getVar(self, varible):
        entorno = self
        while entorno != None:
            if varible in entorno.variables.keys():
                return entorno.variables[varible]
            entorno = entorno.last
        return None
    
    def getFunc(self, funcion):
        if funcion in self.functions.keys():
            return self.functions[funcion]
        else:
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