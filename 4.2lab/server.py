import socket
import threading
import time

# Константы
TCP_HOST = '127.0.0.1'
TCP_PORT = 1500
UDP_GROUP = '233.0.0.1'
UDP_PORT = 1502

# Хранение сообщений
messages = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                messages.append(message)
        except ConnectionResetError:
            break

def broadcast_messages():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    while True:
        if messages:
            message_to_broadcast = "\n".join(messages)
            udp_socket.sendto(message_to_broadcast.encode('utf-8'), (UDP_GROUP, UDP_PORT))
            messages.clear()
        time.sleep(10)

def start_server():
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((TCP_HOST, TCP_PORT))
    tcp_server.listen(5)
    print(f"Сервер запущен на {TCP_HOST}:{TCP_PORT}")

    threading.Thread(target=broadcast_messages, daemon=True).start()

    while True:
        client_socket, addr = tcp_server.accept()
        print(f"Подключен клиент: {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    start_server()