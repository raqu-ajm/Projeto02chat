#(cliente com envio de status)
import socket
import threading
import tkinter as tk

HOST = '127.0.0.1'
PORT = 12345

class ClienteStatus:
    def __init__(self, master):
        self.master = master
        self.master.title("Status do Usuário")
        self.username = input("Digite seu nome de usuário: ")

        self.status_label = tk.Label(master, text="Status: Desconectado", fg="red")
        self.status_label.pack()

        self.chat_area = tk.Text(master, state='disabled', width=50, height=15)
        self.chat_area.pack(pady=5)

        self.entry = tk.Entry(master, width=50)
        self.entry.pack()
        self.entry.bind("<Key>", self.on_typing)

        self.typing_timer = None

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect((HOST, PORT))
            self.client_socket.send(self.username.encode())
            self.status_label.config(text="Status: Conectado", fg="green")
            threading.Thread(target=self.receber_mensagens).start()
        except:
            self.status_label.config(text="Erro ao conectar", fg="red")

    def on_typing(self, event):
        if self.typing_timer:
            self.master.after_cancel(self.typing_timer)
        self.client_socket.send(f"TYPING|{self.username}".encode())
        self.typing_timer = self.master.after(2000, self.stop_typing)

    def stop_typing(self):
        self.client_socket.send(f"STOP_TYPING|{self.username}".encode())

    def receber_mensagens(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                self.chat_area.config(state='normal')
                self.chat_area.insert(tk.END, data + "\n")
                self.chat_area.config(state='disabled')
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteStatus(root)
    root.mainloop()
