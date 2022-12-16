import socket
import threading
import time
from FilaEncadeada import Fila,Head,No
from threading import *
##from Arvore import AVLTree,Node

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users, receives a list with username and client object
filadeespera=Fila()
filadeespera2=Fila()
tosa=[]
medico=[]
semaforo=Semaphore(1)
##Arvore=AVLTree()
# Function to listen for upcoming messages from a client

def listen_for_messages(client, username):
    
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
                    send_message_to_client(client,'SERVER->Seu Pet esta na tosa')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                else:
                    filadeespera.enfileira(username)
                    send_message_to_client(client,f'SERVER->Seu Pet esta na fila de espera, ele esta na {filadeespera.tamanho()}ª posição')
                semaforo.release()
               
            elif message =='2':
                semaforo.acquire()
                if len(medico) < 3:
                    medico.append(username)
                    print(medico)
                    send_message_to_client(client,'SERVER->Seu Pet esta na consulta')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                   
                
                else:
                    filadeespera2.enfileira(username)
                    send_message_to_client(client,f'SERVER->Seu Pet esta na fila de espera, ele esta na {filadeespera2.tamanho()} posição')
                    time.sleep(1.5)
                    cadastro=f'SERVER->Ok! {username}, vamos fazer seu cadastro... Por favor nos informe nome do pet, tipo de pelo e tipo do animal'
                    send_message_to_client(client,cadastro)
                semaforo.release()
            
            if len(message)>7:
                message=message.split(',')
                print(message) #CADASTRO HASH(MESSAGE)
                #arvore.insert(messsage)
                
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
                        #if filadeespra.estavazia():
                        #tosa.append(filadeespera.desenfileira())
                    else:
                        pass
                for i in range(len(medico)):
                    if medico[i]==username:
                        medico.pop(i)
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


if __name__ == '__main__':
    main()
