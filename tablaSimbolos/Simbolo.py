from abstract.Retorno import *

class Simbolo:
    def __init__(self, ids, tipo, position, globalVar, heap):
        self.id = ids
        self.type = tipo
        self.pos = position
        self.isGlobal = globalVar
        self.heap = heap
        self.value = None