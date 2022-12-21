
class User:
    def __init__(self, cpf:any, nome:str):
        self.__cpf = cpf
        self.__nome = nome
        self.__pets = list()
        self.__status='Indefinido'
    
    @property
    def pets(self):
        return self.__pets
    
    @pets.setter
    def pets(self,novoPet):
        self.__pets.append(novoPet)
    
    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def nome(self):
        return self.__nome
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,novoStatus):
        self.__status=novoStatus

    def __str__(self):
        return str(str(self.__cpf) + ' - ' + self.__nome)
