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
LISTENER_LIMIT = 20
active_clients = [] # List of all currently connected users, receives a list with username and client object
fila_tosa=Fila()
fila_vet=Fila()
tosa=list()
medico=list()
usuarios = list()
semaforo=Semaphore(1)
arvore=ArvoreBinaria()
status=''

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
                    usuario=User(cpf,username)
                    script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa"+ '\n2- Agenda Médica' + "\n3- Consultar meu Pet"
                    send_message_to_client(client,script)
                else:
                    send_message_to_client(client,'SERVER-> Percebemos que voce ainda nao tem cadastro...')
                    time.sleep(1)
                    usuario=User(cpf,username)
                    send_message_to_client(client,'SERVER->Nos informe nome do seu pet, tipo do pelo e tipo do animal\n(Ex: bolt,curto,cachorro)')
            if len(message)>7 and message.isnumeric()==False:
                pet=message.split(',') ##array 
                usuario.setPets(pet) #adicionou pet no objeto usuario
                arvore.add(cpf)
                print(arvore.preordem())
                send_message_to_client(client,'SERVER->cadastro concluido com sucesso!')
                time.sleep(1)
                script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa (10 vagas/dia)"+ '\n2- Agenda Médica (10 vagas/dia)' + "\n3- Consultar meu Pet cadastrado"
                send_message_to_client(client,script)



            if message == '1':
                semaforo.acquire()
                if fila_tosa.tamanho()<10:
                    fila_tosa.enfileira(cpf)
                    print(fila_tosa.busca(cpf))
                    semaforo.release()
                    time.sleep(1)
                    
                    if fila_tosa.busca(cpf)==1:
                        status='EM BANHO E TOSA...'
                        send_message_to_client(client,f'SERVER-> {status}')
                        threading.Thread(target=limpaTosa,args=(client, username,)).start()
                    else:
                        status='AGUARDANDO...'
                        send_message_to_client(client,f'SERVER->Seu Pet esta agendado para a {fila_tosa.tamanho()}° tosa! {status}')
                        
                
                else:
                    send_message_to_client(client,'SERVER-> As agendas da tosa hoje estão lotadas... volte amanhã!')
                    
                
               
            elif message =='2':
                semaforo.acquire()
                if fila_vet.tamanho()<10:
                    fila_vet.enfileira(usuario.getNome())
                    print(fila_vet.busca(usuario.getNome()))
                    semaforo.release()
                    time.sleep(1)

                    if fila_tosa.busca(cpf)==1:
                        status='EM BANHO E TOSA...'
                        send_message_to_client(client,f'SERVER-> {status}')
                        threading.Thread(target=limpaTosa,args=(client, username,)).start()
                    else:
                        status='AGUARDANDO...'
                        send_message_to_client(client,f'SERVER->Seu Pet esta agendado para a {fila_tosa.tamanho()}° tosa! {status}')
                        
                else:
                    send_message_to_client(client,'SERVER-> As agendas da consulta veterinária hoje estão lotadas... volte amanhã!')
                    
                
            elif message =='3':
                #pets=usuario.getPets()
               
                send_message_to_client(client,f"SERVER->{username},seu Pet cadastrado é:")
                pets=usuario.getPets()
                time.sleep(1)
                send_message_to_client(client,f'SERVER->{pets[0][0]} e ele esta {status}')
            else:
                pass #ignora caso nao haja mensagem do servidor
            if message== 'QUIT':   
                send_message_to_client(client,'SERVER->Você saiu do chat')
                #active_clients.remove([username, client])
                client.close()
                break
                
        else:
            print(f" SERVER->A mensagem do cliente {username} é vazia")


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
            print("Nome do Cliente esta vazio")
        
    

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
        time.sleep(30)
        status='PRONTO!'
        fila_tosa.desenfileira() #retorna o que saiu da fila
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {status} para ser buscado! \ndigite QUIT para sair do chat')
       
     


def limpaMedico(client,username):
    time.sleep(30)
    fila_vet.desenfileira() #retorna o que saiu da fila
    send_message_to_client(client,f'Server-> Olá {username} Seu pet esta pronto para ser buscado! \ndigite QUIT para sair do chat')




if __name__ == '__main__':
    main()
