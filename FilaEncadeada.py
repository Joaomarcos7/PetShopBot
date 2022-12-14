class FilaException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class No:
    def __init__(self, carga:any):
        self.__carga = carga
        self.__prox = None

    @property
    def carga(self):
        return self.__carga

    @property
    def prox(self):
        return self.__prox

    @carga.setter
    def carga(self, novaCarga):
        self.__carga = novaCarga

    @prox.setter
    def prox(self, novoProx):
        self.__prox = novoProx

    def __str__(self):
        return f'{self.__carga}'


class Head:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

class Fila:
    def __init__(self):
        self.__head = Head()

    def estaVazia(self):
        return self.__head.tamanho == 0

    def tamanho(self):
        return self.__head.tamanho

    def __len__(self):
        return self.__head.tamanho

    
    def enfileira(self, carga:any):
        novo = No(carga)

        if self.estaVazia():
            self.__head.inicio = self.__head.fim = novo
        else:    
            self.__head.fim.prox = novo
            self.__head.fim = novo
        self.__head.tamanho += 1

    def desenfileira(self)->any:
        if self.estaVazia():
            raise FilaException('Fila vazia. Não há elementos para remover.')

        carga = self.__head.inicio.carga
        if self.__head.tamanho == 1:
            self.__head.inicio = self.__head.fim = None
        else:
            self.__head.inicio = self.__head.inicio.prox
        self.__head.tamanho -= 1
        return carga

    def frente(self)->any:
        if self.estaVazia():
            raise FilaException('Fila vazia.')
        return self.__head.inicio.carga

    def busca(self, chave:any)->int:
        # Estrutura para percorrer todos os elementos de uma estrutura linear encadeada
        # cursor = self.__head
        # while( cursor != None ):
        #       ... faz alguma coisa
        #    cursor = cursor.prox
        cont = 1
        cursor = self.__head.inicio
        while( cursor != None ):
            if cursor.carga == chave:
                return cont
            cont += 1
            cursor = cursor.prox

        raise FilaException(f'Chave {chave} não encontrada na Fila')        

    def elemento(self, posicao:int)->any:
        try:
            assert posicao > 0 and posicao <= len(self)
            cont = 1
            cursor = self.__head.inicio
            while( cursor != None ):
                if cont == posicao:
                    break
                cont += 1
                cursor = cursor.prox
            
            return cursor.carga
        except AssertionError:
            raise FilaException('Posicao invalida para a Fila atual')        


    def __str__(self):
        s = 'frente-> [ '
        # código base para percorrer qualquer estrutura linear
        cursor = self.__head.inicio
        while( cursor != None ):
            s += f'{cursor.carga}, '
            # incremento do cursor
            cursor = cursor.prox
        s += ' ]'
        return s