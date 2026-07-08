import socket
import time

SERVER_IP = "127.0.0.1"   # Usa esta IP si el cliente corre en la misma VM
PORT = 9090

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, PORT))
        s.sendall(b"HEARTBEAT")
        data = s.recv(1024)
        print("Respuesta del servidor:", data.decode())
        s.close()
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
