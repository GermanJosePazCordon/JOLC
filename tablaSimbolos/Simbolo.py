from abstract.Retorno import *

class Simbolo:
    def __init__(self, ids, tipo, position, globalVar, heap, vector = "", struct = ""):
        self.id = ids
        self.tipo = tipo #ANTES ESTABA COMO type
        self.pos = position
        self.isGlobal = globalVar
        self.heap = heap
        self.struct = struct
        self.vector = vector
        self.value = None