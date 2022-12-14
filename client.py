import socket
import threading
import tkinter as tk # biblioteca para criar a GUI
from tkinter import scrolledtext
from tkinter import messagebox 

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


# criação objeto socket definindo o tipo de conexão
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adiciona a mensagem na GUI
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)



# Função para o cliente se conectar ao servidor
def connect():

    try:

       
        client.connect((HOST, PORT))
        print("[SERVER] Conectado com sucesso ao servidor")
        add_message("[SERVER] Conectado com sucesso ao servidor")
    except:
        messagebox.showerror("Não foi possível conectar", f"Não foi possível se conectar ao servidor {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Inválido username", "Username não pode ser vazio")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

# Função para mandar mensagem para o servidor
def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
        if message == 'QUIT':
            messagebox.showinfo(title='Sair do chat', message="Você saiu do chat!")          
            root.destroy()
            client.close()
            
    else:
        messagebox.showerror("Mensagem vazia", "Mensagem não pode ser vazia")

# GUI
root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


# Escuta em um loop as mensagens do servidor e formata elas para serem exibidas na GUI.
def listen_for_messages_from_server(client):

    while 1:
            # Recebe a mensagem do servidor
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("->")[0] 
            print(message.split('->'))
            content = message.split("->")[1] # mensagem do cliente
            if content=='QUIT': # se o cliente sair do chat
                add_message("[SERVER]->Cliente saiu do chat")
                client.close() # fecha a conexão
                break

            add_message(f"[{username}] {content}") # exibe a mensagem do cliente na GUI
             
        else:
            messagebox.showerror("Erro", "Messagem do cliente é vazia") 

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()