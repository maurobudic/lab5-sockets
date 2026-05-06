import socket
import threading

HOST = 'localhost'
PORT = 65433

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

name = input("Unesite korisničko ime: ")
sock.sendall(name.encode())

print("Chat započet. Ctrl+C za izlaz.")

def receive():
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("\n" + data.decode())
        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        msg = input("> ")
        sock.sendall(msg.encode())
    except KeyboardInterrupt:
        sock.close()
        break