
class User:
    def __init__(self, count:any, nome:str):
        self.id = count
        self.nome = nome
        self.pets = list()
    
    def __str__(self):
        return str(str(self.id) + ' - ' + self.nome)

    def getPets(self):
        return self.pets
    
    def setPets(self,novoPet):
        self.pets.append(novoPet)
    
    def getId(self):
        return self.id
    
    def getNome(self):
        return self.nome