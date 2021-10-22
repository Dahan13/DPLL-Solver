__author__ = 'Gastaldi'
__Filename__ = 'Pile'
__Creationdate__ = '15/10/2020'


class PileCNF(object):

    def __init__(self):
        self.Literral = []
        self.Val = []

    def getLit(self)-> list:
        return self.Literral

    def setLit(self, x):
        self.Literral = x

    def getVal(self) -> list:
        return self.Val

    def setVal(self,x):
        self.Val = x

    def DelLast(self):
        if len(self.getVal()) > 0 and len(self.getLit()) > 0:
            self.setLit(self.getLit()[:-1])
            self.setVal(self.getVal()[:-1])

    def Pil(self, lit, val):
        self.setLit(self.getLit() + [lit])
        self.setVal(self.getVal() + [val])

    def Pop(self):
        if len(self.Literral) == 0:
            return False, False
        else:
            lit = self.Literral[-1]
            val = self.Val[-1]
            self.DelLast()
            return lit, val

    def ValLit(self, lit):
        for i in range(len(self.getLit())):
            if lit == self.getLit()[i]:
                return self.getVal()[i]
        return None