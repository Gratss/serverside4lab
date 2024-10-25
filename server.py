import socket
import threading
import time

# Конфигурация
TCP_IP = '127.0.0.1'
TCP_PORT = 12345
UDP_IP = '233.0.0.1'
UDP_PORT = 1502

messages = []
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

def tcp_client_handler(tcp_socket):
    global messages
    while True:
        try:
            message = tcp_socket.recv(1024).decode()
            if message:
                messages.append(message)
        except ConnectionResetError:
            break
    tcp_socket.close()

def udp_broadcaster():
    global messages
    while True:
        time.sleep(10)
        if messages:
            payload = "\n".join(messages).encode()
            udp_sock.sendto(payload, (UDP_IP, UDP_PORT))
            messages.clear()

def start_server():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((TCP_IP, TCP_PORT))
    tcp_sock.listen(5)
    print(f"Сервер запущен на {TCP_IP}:{TCP_PORT}")
    
    threading.Thread(target=udp_broadcaster, daemon=True).start()  # Запуск UDP-рассылки в фоновом потоке
    
    while True:
        client_sock, addr = tcp_sock.accept()
        print(f"Подключение от {addr}")
        threading.Thread(target=tcp_client_handler, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()
