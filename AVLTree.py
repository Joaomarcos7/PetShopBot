# Classe que implementa as operações básicas de uma Árvore AVL
# Código Original: 
#  https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
#  https://www.geeksforgeeks.org/avl-tree-set-2-deletion/?ref=lbp
# Adaptações feitas pelo professor Alex para a disciplina de Estrutura de Dados
# Última modificação: 17/05/2022
  
class Node(object): 
    '''Class used to create a generic tree node instance in memory'''
    def __init__(self, value): 
        self.value = value 
        self.left = None
        self.right = None
        self.height = 1 # atributo que especifica a altura que determina o fator de balanco do nó
    
    def __str__(self):
        return f'|{self.value}:h={self.height}|'
  
# Classe AVL tree 
class AVLTree(object): 
    """ Class that creates a AVL tree in memory. AVL tree is a self-balancing
        Binary Search Tree (BST) where the difference between heights
        of left and right subtrees cannot be more than one for all nodes. 
    """

    def __init__(self, value:object = None):
        """ Constructor of the AVL tree object
            Arguments
            ----------------
            value (object): the content to be added to AVL tree. If a value
                            is not provided, the tree initializes "empty".
                            Otherwise, the root node will be the node created
                            to the "value" object.
        """
        if value is None:
            self.__root = None
        else:
            self.__root = self.insert(value)

    def isEmpty(self)->bool:
        '''Method that verifies the AVL Tree is empty or not.

        Returns
        ---------
        True: AVL Tree is empty
        False: AVL Tree is not empty, i.e., there is at least a root node.
        '''
        return self.__root == None

    def insert(self, key:object):
        ''' Insert a new node in AVL Tree recursively from root. The node will be created with
            "key" as value.
        '''
        if(self.__root == None):
            self.__root = Node(key)
        else:
            self.__root = self.__insert(self.__root, key)
  
    def __insert(self, root, key):
        # Step 1 - Performs a BST recursion to add the node
        if not root: 
            return Node(key) 
        elif key < root.value: 
            root.left = self.__insert(root.left, key) 
        else: 
            root.right = self.__insert(root.right, key) 
  
        # Step 2 - Update the height of ancestor node
        root.height = 1 + max(self.getHeight(root.left), 
                              self.getHeight(root.right)) 
  
        # Step 3 - Computes the balance factor 
        balance = self.getBalance(root) 
  
        # Step 4 - Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # CASE 1 - Right rotation
        if balance > 1 and key < root.left.value: 
            return self.__rightRotate(root) 
  
        # CASE 2 - Left rotation
        if balance < -1 and key > root.right.value: 
            return self.__leftRotate(root) 
  
        # CASE 3 - Double rotation: Left Right 
        if balance > 1 and key > root.left.value: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # CASE 4 - Double rotation: Right Left 
        if balance < -1 and key < root.right.value: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 
  
    def __leftRotate(self, p:Node)->Node: 
        """
        Realiza a rotação 'à esquerda' tomando o no 'p' como base
        para tornar 'u' como nova raiz        
        """
 
        u = p.right 
        T2 = u.left 
  
        # Perform rotation 
        u.left = p 
        p.right = T2 
  
        # Update heights 
        p.height = 1 + max(self.getHeight(p.left), 
                         self.getHeight(p.right)) 
        u.height = 1 + max(self.getHeight(u.left), 
                         self.getHeight(u.right)) 
  
        # Return the new root "u" node 
        return u 
  
    def __rightRotate(self, p:Node)->Node: 
        """ Realiza a rotação à direita tomando o no "p" como base
            para tornar "u" como nova raiz
        """
  
        u = p.left 
        T2 = u.right 
  
        # Perform rotation 
        u.right = p 
        p.left = T2 
  
        # Update heights 
        p.height = 1 + max(self.getHeight(p.left), 
                        self.getHeight(p.right)) 
        u.height = 1 + max(self.getHeight(u.left), 
                        self.getHeight(u.right)) 
  
        # Return the new root ("u" node)
        return u 
  
    def getHeight(self, node:Node)->int: 
        """ Obtém a altura relativa ao nó passado como argumento
            Argumentos:
            -----------
            node (Node): o nó da árvore no qual se deseja consultar a altura
            
            Retorno
            -----------
            Retorna um número inteiro representando a altura da árvore
            representada pelo nó "node". O valor 0 significa que o "node"
            não é um objeto em memória
        """
        if node is None: 
            return 0
  
        return node.height 
  
    def getBalance(self, node:Node)->int: 
        """
        Calcula o valor de balanceamento do nó passado como argumento.

        Argumentos:
        -----------
        node (object): o nó da árvore no qual se deseja determinar o 
                       balanceamento
            
        Retorno
        -----------
        Retorna o fator de balanceamento do nó em questão.
        Um valor 0, +1 ou -1 indica que o nó está balanceado
        """
        if not node: 
            return 0
  
        return self.getHeight(node.left) - self.getHeight(node.right) 
  
    def preOrder(self):
        self.__preOrder(self.__root)

    def __preOrder(self, root): 
        if not root: 
            return
  
        print("{0} ".format(root.value), end="") 
        self.__preOrder(root.left) 
        self.__preOrder(root.right) 

    def delete(self, key:object):
        if(self.__root is not None):
            self.__root = self.__delete(self.__root, key)
        

    def __delete(self, root:Node, key:object)->Node: 
        """
        Recursive function to delete a node with given key from subtree
        with given root.

        Retorno
        --------------
        It returns root of the modified subtree.
        """
        # Step 1 - Perform standard BST delete 
        if not root: 
            return root   
        elif key < root.value: 
            root.left = self.__delete(root.left, key)   
        elif key > root.value: 
            root.right = self.__delete(root.right, key)   
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
  
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
  
            temp = self.getMinValueNode(root.right) 
            root.value = temp.value 
            root.right = self.__delete(root.right, 
                                      temp.value) 
  
        # If the tree has only one node, 
        # simply return it 
        if root is None: 
            return root 
  
        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
  
        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 
  
        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.__rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.__leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root  

    def getRoot(self)->Node :
        return self.__root
    
    def getMinValueNode(self, root:Node)->Node:
        """
        Método que obtem o nó de menor valor a partir do 'root'
        passado como argumento (nó mais à esquerda)
        """
        if root is None or root.left is None:
            return root
 
        return self.getMinValueNode(root.left)
  
if __name__ == '__main__':
    
    myTree = AVLTree() 
'''
    
    nums = [42, 15, 88, 6, 27, 4] # right rotation
    for node in nums:
        myTree.insert(node)
   
    # 1. rotação à direita             2. rotação à esquerda
    # 3. rotação à esquerda + direita  4. rotação à direita + esquerda
    TESTE = 1

    if TESTE == 1:
        myTree.insert(42)
        myTree.insert(15)
        myTree.insert(88)
        myTree.insert(6)
        myTree.insert(27)
        myTree.insert(4)
        myTree.preOrder() 
        print()
        """
    The constructed AVL Tree would be 
            15 
           /  \ 
         06   42 
        /    /  \ 
       04   27   88
        """

    elif TESTE == 2:
        myTree.insert(120)
        myTree.insert(100)
        myTree.insert(130)
        myTree.insert(80)
        myTree.insert(110)
        myTree.insert(150)
        myTree.insert(200)
        myTree.preOrder()   
    elif TESTE == 3:
        myTree.insert(120)
        myTree.insert(110)
        myTree.insert(150)
        myTree.insert(80)
        myTree.insert(130)
        myTree.insert(200)
        myTree.insert(100) # nó que provoca o balanceamento
        myTree.preOrder()  

    # teste de remoção
    key = 15
    if TESTE == 1:
        print()
        myTree.preOrder()
        print('Removendo o nó', key)
        root = myTree.delete(key)
        myTree.preOrder()
'''

#    quit()
 

