import socket
import threading
import time
from FilaEncadeada import Fila
from threading import Thread, Semaphore
from ArvoreBinariaBusca import ArvoreBinaria
from user import User

#GLOBAIS

HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 20
active_clients = [] 
fila_tosa = Fila()    # fila para tosa
fila_vet = Fila()     # fila para consulta veterinária
semaforo = Semaphore(1)
arvore = ArvoreBinaria()
status = ''



# Função para escutar as mensagens enviadas por um cliente

def listen_for_messages(client, username):
    
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '->' + message # concatena o nome do usuario com a mensagem
            send_message_to_client(client,final_msg)
            if message.isnumeric() and len(message)>10: # verifica se o a mensagem é um cpf
                cpf=message
                if arvore.busca(cpf): # verifica se o cpf já está cadastrado
                    send_message_to_client(client,f'SERVER-> Olá Seja bem vindo de volta {username}!')
                    time.sleep(1)
                    for i in active_clients: # itera sobre a lista de clientes ativos para buscar seu objeto USER
                        if i.cpf==cpf:
                            usuario=i
                    script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa"+ '\n2- Agenda Médica' + "\n3- Consultar meu Pet"
                    send_message_to_client(client,script)
                else:
                    semaforo.acquire()
                    send_message_to_client(client,'SERVER-> Percebemos que voce ainda nao tem cadastro...')
                    time.sleep(1)
                    usuario=User(cpf,username) # cria um objeto USER
                    arvore.add(cpf) # adiciona o cpf na estrutura de arvore
                    active_clients.append(usuario) # adiciona o objeto na lista de clientes ativos
                    send_message_to_client(client,'SERVER->Nos informe nome do seu pet, tipo do pelo e tipo do animal\n(Ex: bolt,curto,cachorro)')
                    semaforo.release()
            if len(message)>7 and message.isnumeric()==False: # verifica se a mensagem é um PET
                pet=message.split(',') # separa a mensagem em uma lista
                usuario.pets=pet    # adiciona o pet na lista de pets do usuario
                send_message_to_client(client,'SERVER->cadastro concluido com sucesso!')
                time.sleep(1)
                script="SERVER-> Oferecemos varios serviços... por favor nos indique qual voce gostaria de usufruir:" + "\n1- Banho e Tosa (10 vagas/dia)"+ '\n2- Agenda Médica (10 vagas/dia)' + "\n3- Consultar meu Pet cadastrado" 
                send_message_to_client(client,script)



            if message == '1':
                semaforo.acquire()
                if fila_tosa.temlimite()==True: # verifica se a fila de tosa tem vagas
                    fila_tosa.enfileira(cpf)
                    print(fila_tosa.busca(cpf))
                    semaforo.release()
                    time.sleep(1)
                    
                    if fila_tosa.busca(cpf) == 1: # verifica se o usuario é o primeiro da fila
                        usuario.status='EM TOSA...' 
                        send_message_to_client(client,f'SERVER-> Você é o primeiro da fila! entao seu pet ja está {usuario.status}')
                        threading.Thread(target=limpaTosa,args=(client, username,usuario)).start() # chama a função limpaTosa em uma thread para que haja contagem do pet na tosa e desfileire.
                    else:
                        usuario.status='AGUARDANDO...'
                        send_message_to_client(client,f'SERVER-> Seu Pet está agendado para a {fila_tosa.tamanho()}° tosa! Status: {usuario.status}')
                        threading.Thread(target=limpaTosa,args=(client, username,usuario)).start()
                        
                        
                
                else: # se a fila de tosa estiver lotada
                    send_message_to_client(client,'SERVER-> As agendas da tosa hoje estão lotadas... volte amanhã! \nDigite [QUIT] para sair')
                    
                
               
            elif message =='2': 
                semaforo.acquire()
                if fila_vet.temlimite()==True:
                    fila_vet.enfileira(cpf)
                    print(fila_vet.busca(cpf))
                    semaforo.release()
                    time.sleep(1)

                    if fila_vet.busca(cpf) == 1:
                        usuario.status='EM CONSULTA...'
                        send_message_to_client(client,f'SERVER-> Você é o primeiro da fila! entao seu pet ja está {usuario.status}')
                        threading.Thread(target=limpaMedico,args=(client, username,usuario)).start() # chama a função limpaMedico em uma thread para que haja contagem do pet na consulta e desfileire.
                    else:
                        usuario.status='AGUARDANDO...'
                        send_message_to_client(client,f'SERVER-> Seu Pet esta agendado para a {fila_tosa.tamanho()}° tosa! Status: {usuario.status}')
                        threading.Thread(target=limpaMedico,args=(client, username,usuario)).start()
                        
                else:
                    send_message_to_client(client,'SERVER-> As agendas da consulta veterinária hoje estão lotadas... volte amanhã! \nDigite [QUIT] para sair')
                    
                
            elif message =='3':    # verifica se o usuario quer consultar seu pet
                send_message_to_client(client,f"SERVER-> {username},seu Pet cadastrado é:")
                pets=usuario.pets # pega a lista de pets do usuario
                time.sleep(1)
                send_message_to_client(client,f'SERVER-> {pets[0][0]} e seu status é {usuario.status}')
            else:
                pass # ignora caso nao haja mensagem do servidor
            if message == 'QUIT':   
                send_message_to_client(client,'SERVER-> Você saiu do chat')
                client.close()
                break
                
        else:
            print(f" SERVER-> A mensagem do cliente {username} é vazia")


# Função para Enviar Mensagem a um cliente

def send_message_to_client(client, message):
    client.sendall(message.encode()) # envia a mensagem para o cliente

# Função para tratar o cliente
def client_handler(client):
    
    # Server vai lidar com o username do cliente e dar o script de boas vindas
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
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
        
    
# Thread- Função para ouvir as mensagens dos clientes
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# MAIN 
def main():

    # Criação socket objeto 
    # AF_INET:  utilizando endereços IPV4
    # SOCK_STREAM: utlizando Protocolo TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    try:
        # Conecta o server ao host e porta e tenta rodar o server
        server.bind((HOST, PORT))
        print(f"Server rodando em  {HOST} {PORT}")
    except:
        print(f"Incapaz de rodar o server no host {HOST} e na porta {PORT}")

    # Define o limite de conexões
    server.listen(LISTENER_LIMIT)

        # Loop para ficar escutando as conexões dos clientes!
    while 1:

        client, address = server.accept() #retorna uma array com o cliente e o endereço
        print(f"Conectado ao cliente {address[0]} {address[1]}")

    # Thread- Função para tratar o cliente
        threading.Thread(target=client_handler, args=(client, )).start()


# Desinfileira a fila da tosa e define que o pet esta pronto para ser buscado

def limpaTosa(client,username,usuario):

    if usuario.status == "AGUARDANDO...":
        time.sleep(12)
        usuario.status = "EM TOSA..."
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status}!')
        time.sleep(12)
        usuario.status = "PRONTO"
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status} para ser buscado! \ndigite [QUIT]para sair do chat')
    else:
        time.sleep(12)
        usuario.status='PRONTO'
        fila_tosa.desenfileira() #retorna o que saiu da fila
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status} para ser buscado! \ndigite [QUIT]para sair do chat')
       
     
# Desinfileira a fila do Vet e define que o pet esta pronto para ser buscado

def limpaMedico(client,username,usuario):
    if usuario.status == "AGUARDANDO...":
        time.sleep(12)
        usuario.status = "EM CONSULTA..."
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status}!')
        time.sleep(12)
        usuario.status = "PRONTO"
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status} para ser buscado! \ndigite [QUIT]para sair do chat')
    else:
        time.sleep(12)
        usuario.status='PRONTO'
        fila_tosa.desenfileira() #retorna o que saiu da fila
        send_message_to_client(client,f'Server-> Olá {username} Seu pet esta {usuario.status} para ser buscado! \ndigite [QUIT]para sair do chat')


# rodando todo o main()!

if __name__ == '__main__':
    main()
