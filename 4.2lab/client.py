import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Константы
TCP_HOST = '127.0.0.1'
TCP_PORT = 1500
UDP_GROUP = '233.0.0.1'
UDP_PORT = 1502

# Отправка сообщения на сервер
def send_message():
    message = message_entry.get()
    if message:
        tcp_socket.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

# Получение широковещательных сообщений
def receive_messages():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.bind(('', UDP_PORT))
    group = socket.inet_aton(UDP_GROUP)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, group + socket.inet_aton('0.0.0.0'))

    while True:
        message, _ = udp_socket.recvfrom(1024)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, message.decode('utf-8') + '\n')
        chat_area.config(state=tk.DISABLED)

# Настройка графического интерфейса
root = tk.Tk()
root.title("Чат-приложение")

chat_area = scrolledtext.ScrolledText(root, state='disabled')
chat_area.pack(pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)

send_button = tk.Button(root, text="Отправить", command=send_message)
send_button.pack(pady=10)

# Создание TCP-сокета
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_HOST, TCP_PORT))

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()