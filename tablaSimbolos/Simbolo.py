from abstract.Retorno import *

class Simbolo:
    def __init__(self, ids, tipo, position, globalVar, heap, struct = ""):
        self.id = ids
        self.type = tipo
        self.pos = position
        self.isGlobal = globalVar
        self.heap = heap
        self.struct = struct
        self.value = None