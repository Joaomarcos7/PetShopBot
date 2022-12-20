import socket
import threading
import time
from FilaEncadeada import Fila,Head,No
from threading import Thread, Semaphore
from ArvoreBinariaBusca import ArvoreBinaria
from user import User
#from arvore import AVLTree
##from Arvore import AVLTree,Node

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users, receives a list with username and client object
fila_tosa=Fila()
fila_vet=Fila()
tosa=list()
medico=list()
usuarios = list()
semaforo=Semaphore(1)
arvore=ArvoreBinaria()

#arvore=AVLTree()
##Arvore=AVLTree()

# Function to listen for upcoming messages from a client

def listen_for_messages(client, username):
    
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '->' + message
            send_message_to_client(client,final_msg)
            if message.isnumeric() and len(message)>10:
                cpf=message
                if arvore.busca(cpf):
                    send_message_to_client(client,f'SERVER-> Olá Seja bem vindo de volta {username}!')
                    time.sleep(1)
                    script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa"+ '\n2- Agenda Médica' + "\n3 Consultar meu Pet"
                    send_message_to_client(client,script)
                else:
                    send_message_to_client(client,'SERVER-> Percebemos que voce ainda nao tem cadastro...')
                    time.sleep(1)
                    send_message_to_client(client,'SERVER->Nos informe nome do seu pet, tipo do pelo e tipo do animal\n(Ex: bolt,curto,cachorro)')
            if len(message)>7 and message.isnumeric()==False:
                pet=message.split(',') ##array
                usuario=User(cpf,username) #criacao usuario
                usuario.setPets(pet)
                
                arvore.add(cpf)
                print(arvore.preordem())
                send_message_to_client(client,'SERVER->cadastro concluido com sucesso!')
                time.sleep(1)
                script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa"+ '\n2- Agenda Médica' + "\n3 Consultar meu Pet"
                send_message_to_client(client,script)



            if message == '1':
                semaforo.acquire()
                if fila_tosa.tamanho()<10:
                    fila_tosa.enfileira(usuario.getNome())
                    semaforo.release()
                    time.sleep(1)
                    send_message_to_client(client,f'SERVER->Seu Pet esta agendado para a {fila_tosa.tamanho()}° tosa!')
                
                else:
                    send_message_to_client(client,'SERVER-> As agendas da tosa hoje estão lotadas... volte amanhã!')
                    
                threading.Thread(target=limpaTosa,args=(client, username, )).start()
               
            elif message =='2':
                semaforo.acquire()
                if fila_vet.tamanho()<10:
                    fila_vet.enfileira(usuario.getNome())
                    semaforo.release()
                    time.sleep(1)
                    send_message_to_client(client,f'SERVER->Seu Pet esta agendado para a {fila_vet.tamanho()}° tosa!')
                
                else:
                    send_message_to_client(client,'SERVER-> As agendas da consulta veterinária hoje estão lotadas... volte amanhã!')
                    
                threading.Thread(target=limpaTosa,args=(client, username, )).start()
            
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
                    

                #print(message) #CADASTRO HASH(MESSAGE)
                #arvore.insert(messsage)
                #       
            else:
                pass
            if message== 'QUIT':   
                for i in range(len(tosa)):
                    if tosa[i]==username:
                        tosa.pop(i)
                        print(tosa)
                        #if filadeespera.estaVazia() == False:
                            #tosa.insert(i,filadeespera.desenfileira())
                    else:
                        pass
                for i in range(len(medico)):
                    if medico[i]==username:
                        medico.pop(i)
                        #if filadeespera2.estaVazia() == False:
                            #medico.insert(i,filadeespera2.desenfileira())
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
            pergunta='SERVER ->' + 'Nos informe seu CPF:'
            send_message_to_client(client,welcome)
            time.sleep(1.5)
            send_message_to_client(client,pergunta)
            
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
        

def limpaTosa(client,username):
    #while filadeespera.estaVazia() == False:   
        time.sleep(60)
        for i in tosa:
            if i==username:
                tosa.pop(i)
        #proximo = filadeespera.desenfileira()
       # tosa.append(proximo)
        send_message_to_client(client,'Server- Chegou sua vez! Voce esta no medico agora...')
        print(tosa)


def limpaMedico(client,username):
   # while filadeespera2.estaVazia() == False:   
        time.sleep(60)
        for i in medico:
            if i==username:
                medico.pop(i)
      #  proximo = filadeespera2.desenfileira()
      #  medico.append(proximo)
        send_message_to_client(client,'Server- Chegou sua vez! Voce esta no medico agora...')
        print(medico)





if __name__ == '__main__':
    main()
