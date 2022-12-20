
class User:
    def __init__(self, cpf:any, nome:str):
        self.__cpf = cpf
        self.__nome = nome
        self.__pets = list()
    

    def getPets(self):
        return self.__pets
    

    def setPets(self,novoPet):
        self.__pets.append(novoPet)
    
    @property
    def getCpf(self):
        return self.__cpf
    
    @property
    def getNome(self):
        return self.__nome

    def __str__(self):
        return str(str(self.__cpf) + ' - ' + self.__nome)
