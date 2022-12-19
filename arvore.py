from enum import Enum

class No:
    def __init__(self,carga:any):
        self.carga = carga
        self.esq = None
        self.dir = None

    def __str__(self):
        return str(self.carga)

 
class Origem(Enum):
    RAIZ = 1
    CURSOR = 2

class ArvoreBinaria:        
    def __init__(self, carga_da_raiz:any = None):
        self.__raiz = No(carga_da_raiz) if carga_da_raiz != None else carga_da_raiz
        print(self.__raiz)
        self.__cursor = self.__raiz

    def criarRaiz(self, carga_da_raiz:any):
        if self.__raiz is None:
            self.__raiz = No(carga_da_raiz)

    def estaVazia(self)->bool:
        return self.__raiz == None
        
    def getRaiz(self)->any:
        if self.__raiz is not None:
            return self.__raiz.carga
        else:
            return None

    def getCursor(self)->any:
        if self.__cursor is not None:
            return self.__cursor.carga
        else:
            return None

    def preordem(self, origem:Origem = Origem.RAIZ):
        if origem == Origem.RAIZ:
            self.__preordem(self.__raiz)
        elif origem == Origem.CURSOR:
            self.__preordem(self.__cursor)

    def __preordem(self, no):
        if no is None:
            return
        print(f'{no.carga}', end=' ')
        self.__preordem(no.esq)
        self.__preordem(no.dir)

    def emordem(self):
        self.__emordem(self.__raiz)

    def __emordem(self, no):
        if no is None:
            return
        self.__emordem(no.esq)
        print(f'{no.carga}', end=' ')
        self.__emordem(no.dir)

    def posordem(self):
        self.__posordem(self.__raiz)

    def __posordem(self, no):
        if no is None:
            return
        self.__posordem(no.esq)
        self.__posordem(no.dir)
        print(f'{no.carga}', end=' ')


    def descerEsquerda(self):
        if self.__cursor is not None and \
           self.__cursor.esq is not None:
           self.__cursor = self.__cursor.esq

    def descerDireita(self):
        if self.__cursor is not None and \
           self.__cursor.dir is not None:
           self.__cursor = self.__cursor.dir

    def resetCursor(self):
        self.__cursor = self.__raiz

    def addFilhoEsquerdo(self, carga)->bool:
        if self.__cursor is not None:
            if self.__cursor.esq is None:
                self.__cursor.esq = No(carga)
                return True
        else:
            return False
    
    def addFilhoDireito(self, carga)->bool:
        if self.__cursor is not None:
            if self.__cursor.dir is None:
                self.__cursor.dir = No(carga)
                return True
        else:
            return False

    def __count(self, no:No)->int:
        
        if no is None:
            return 0
        return 1 + self.__count(no.esq)+self.__count(no.dir)
        

    def __len__(self):
        return self.__count(self.__raiz)

    def busca(self, chave:any ):
        return self.__busca(chave, self.__raiz)
    
    def __busca(self, chave, no:No):
        if no is None:
            return False
        if no.carga == chave:
            return True
        if ( self.__busca(chave, no.esq)):
            return True
        else:
            return self.__busca(chave, no.dir)

    def removeNo(self, chave:any):
        if self.__cursor is None:
            return
        # verificar se a chave esta na esquerda ou na direita do cursor
        if self.__cursor.esq is not None and self.__cursor.esq.carga == chave:
            if self.__cursor.esq.esq == None and \
               self.__cursor.esq.dir == None:
                self.__cursor.esq = None

        elif self.__cursor.dir is not None and self.__cursor.dir.carga == chave:
            if self.__cursor.dir.esq == None and \
               self.__cursor.dir.dir == None:
                self.__cursor.dir = None


        
    def go(self, chave:int )->No:
        return self.__go(chave,self.__raiz)
    
    def __go(self, chave:int, no:No)->No:
        if no is None:
            return None
        if no.carga == chave:
            return no
        resultado = self.__go(chave, no.esq)
        if ( resultado ):
            return resultado
        else:
            return self.__go(chave, no.dir)


    def  removeRaiz(self)->bool:
        '''Só remove a raiz se a árvore tiver apenas a raiz'''
        if (len(self) == 1):
            self.__raiz = self.__cursor = None
            return True
        else:
            return False

        
if __name__=='__main__':

    arvore = ArvoreBinaria('PET')
    arvore.addFilhoEsquerdo('CACHORRO')
    arvore.addFilhoDireito('GATO')
    arvore.descerEsquerda()
    arvore.addFilhoEsquerdo('PEQUENO')
    arvore.addFilhoDireito('GRANDE')
    arvore.descerEsquerda()
    arvore.addFilhoEsquerdo([])
    arvore.resetCursor()
    arvore.descerEsquerda()
    arvore.descerDireita()
    arvore.addFilhoEsquerdo([])
    arvore.resetCursor()
    arvore.descerDireita()
    arvore.addFilhoEsquerdo('PEQUENO')
    arvore.addFilhoDireito('GRANDE')
    arvore.descerEsquerda()
    arvore.addFilhoEsquerdo([])
    arvore.resetCursor()
    arvore.descerDireita()
    arvore.descerDireita()
    arvore.addFilhoEsquerdo([])

    print(arvore.preordem())
    # animal com nome e código gerado pelo servidor para marcar ele unique key

    '''
                                                PET
                            CACHORRO                                  GATO
                GRANDE                  PEQUENO             GRANDE                  PEQUENO
            list()                       list()             list()                  list()


    '''
            
    
