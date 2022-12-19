import socket
import threading
import time
from FilaEncadeada import Fila,Head,No
from threading import Thread, Semaphore
from AVLTree import AVLTree
from user import User
#from arvore import AVLTree
##from Arvore import AVLTree,Node

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users, receives a list with username and client object
filadeespera=Fila()
filadeespera2=Fila()
tosa=list()
medico=list()
cadastro_clientes = AVLTree()
usuarios = list()
semaforo=Semaphore(1)

#arvore=AVLTree()
##Arvore=AVLTree()

# Function to listen for upcoming messages from a client

def listen_for_messages(client, username):
    id_user = 0
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '->' + message
            send_message_to_client(client,final_msg)
            if message == '1':
                semaforo.acquire()
                if len(tosa) < 3:
                    tosa.append(username)
                    print(tosa)
                    semaforo.release()
                    send_message_to_client(client,'SERVER->Seu Pet esta na tosa')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                else:
                    
                    filadeespera.enfileira(username)
                    tamfila=filadeespera.tamanho()
                    semaforo.release()
                    send_message_to_client(client,f'SERVER->Seu Pet esta na fila de espera, ele esta na {tamfila}ª posição')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                    threading.Thread(target=limpaTosa).start()
                semaforo.release()
               
            elif message =='2':
                semaforo.acquire()
                if len(medico) < 3:
                    medico.append(username)
                    print(medico)
                    semaforo.release()
                    send_message_to_client(client,'SERVER->Seu Pet esta na consulta')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)                  
                
                else:
                    filadeespera2.enfileira(username)
                    tamfila2=filadeespera2.tamanho()
                    semaforo.release()
                    send_message_to_client(client,f'SERVER->Seu Pet esta na fila de espera, ele esta na {tamfila2} posição')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                    threading.Thread(target=limpaMedico).start()
                semaforo.release()
            
            elif message =='3':
                achouUsuario = False
                for usuario in usuarios:
                    if usuario.getNome() == username:
                        achouUsuario = True
                        info = 'SERVER->Seus pets são: '
                        send_message_to_client(client,info)
                        time.sleep(2)
                        for pet in usuario.getPets():
                            my_pet = str(pet[0] + ' - ' + pet[1] + ' - ' + pet[2])
                            send_message_to_client(client, 'SERVER->' + my_pet)
                
                if not(achouUsuario):
                    send_message_to_client(client, "SERVER->Você ainda não cadastrou um pet!")
                    

            if len(message)>7:
                message=message.split(',')
                encontrouUsuario = False
                for u in usuarios:
                    if u.getNome() == username:
                        encontrouUsuario = True
                        u.setPets(list(message))
                
                if not(encontrouUsuario):
                    id_user += 1
                    novo_usuario = User(id_user,username)
                    novo_usuario.setPets(list(message))

                    cadastro_clientes.insert(novo_usuario.getId())
                    usuarios.append(novo_usuario)

                #print(message) #CADASTRO HASH(MESSAGE)
                #arvore.insert(messsage)
                #        
                time.sleep(1.5)
                conclusao='SERVER->Cadastro concluído com sucesso! Obrigado pela confiança!'
                send_message_to_client(client,conclusao)
            else:
                pass
            if message == 'QUIT':   
                for i in range(len(tosa)):
                    if tosa[i]==username:
                        tosa.pop(i)
                        print(tosa)
                        if filadeespera.estaVazia() == False:
                            tosa.insert(i,filadeespera.desenfileira())
                    else:
                        pass
                for i in range(len(medico)):
                    if medico[i]==username:
                        medico.pop(i)
                        if filadeespera2.estaVazia() == False:
                            medico.insert(i,filadeespera2.desenfileira())
                send_message_to_client(client,'SERVER->Você saiu do chat')
                
                break
                
        else:
            print(f" SERVER->The message send from client {username} is empty")


# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER->" + f"{username} added to the chat"
            send_message_to_client(client,prompt_message)
            welcome='SERVER->' + f"Olá {username} Seja bem vindo ao nosso Pet Shop!"
            script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa"+ '\n2- Agenda Médica' + "\n3 Consultar meu Pet" + "\n QUIT- para logout do server"
            send_message_to_client(client,welcome)
            time.sleep(1.5)
            send_message_to_client(client,script)
            
            break
        else:
            print("Client username is empty")
        
    

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")


        threading.Thread(target=client_handler, args=(client, )).start()
        

def limpaTosa():
    while filadeespera.estaVazia() == False:   
        time.sleep(30)
        tosa.clear()
        proximo = filadeespera.desenfileira()
        tosa.append(proximo)
        print(tosa)

def limpaMedico():
    while filadeespera2.estaVazia() == False:   
        time.sleep(30)
        medico.clear()
        proximo = filadeespera2.desenfileira()
        medico.append(proximo)
        print(medico)

if __name__ == '__main__':
    main()
