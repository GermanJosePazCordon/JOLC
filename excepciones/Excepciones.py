import time

class Excepciones:
    def __init__(self, tipo, sms, row, column):
        self.tipo = tipo
        self.sms = sms
        self.row = row
        self.column = column
        self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def toString(self):
        return str(self.tipo) + " - " + str(self.sms) + " : [" + str(self.row) + ", " + str(self.column) + "]" 
    
    def show(self):
        return self.toString() + "\n"
    
    def getTipo(self):
        return self.tipo
    
    def getSMS(self):
        return self.sms
    
    def getRow(self):
        return self.row
    
    def getColumn(self):
        return self.column