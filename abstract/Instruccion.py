from abc import ABC, abstractmethod
from tablaSimbolos.Simbolo import Simbolo

class Instruccion(ABC):
    def __init__(self, tipo, row, column):
        super().__init__()
        self.tipo = tipo
        self.row = row
        self.column = column
        self.ev = ''
        self.ef = ''

    @abstractmethod
    def interpretar(self, tree, table):
        pass

    @abstractmethod
    def getNodo(self):
        pass