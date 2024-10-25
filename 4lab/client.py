import socket
import threading
import tkinter as tk

# Конфигурация
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
UDP_IP = '233.0.0.1'
UDP_PORT = 1502

def receive_messages():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    udp_sock.bind(('', UDP_PORT))
    
    while True:
        data, _ = udp_sock.recvfrom(1024)
        message_display.insert(tk.END, data.decode() + '\n')

def send_message():
    message = message_input.get()
    message_input.delete(0, tk.END)
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((TCP_IP, TCP_PORT))
    tcp_sock.sendall(message.encode())
    tcp_sock.close()

# GUI
root = tk.Tk()
root.title("Чат")

message_input = tk.Entry(root, width=50)
message_input.pack(pady=10)

send_button = tk.Button(root, text="Отправить", command=send_message)
send_button.pack(pady=5)

message_display = tk.Text(root, width=50, height=15)
message_display.pack(pady=10)

# Запуск потока для получения сообщений
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
