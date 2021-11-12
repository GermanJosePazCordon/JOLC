from abstract.Retorno import *

class Simbolo:
    def __init__(self, ids, tipo, position, globalVar, heap, vector = "", struct = "", row = "", column = ""):
        self.id = ids
        self.tipo = tipo #ANTES ESTABA COMO type
        self.pos = position
        self.isGlobal = globalVar
        self.heap = heap
        self.struct = struct
        self.vector = vector
        self.value = None
        self.row = row
        self.column = column