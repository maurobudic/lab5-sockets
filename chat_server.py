import selectors
import socket
import time

sel = selectors.DefaultSelector()
clients = {}

HOST = 'localhost'
PORT = 65433

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
lsock.setblocking(False)

sel.register(lsock, selectors.EVENT_READ)

print(f"[CHAT SERVER] Listening on {HOST}:{PORT}")

last_print = time.time()

def log(msg):
    with open("chat.log", "a") as f:
        f.write(msg + "\n")

while True:
    events = sel.select(timeout=1)

    if time.time() - last_print > 10:
        print(f"[INFO] Aktivni korisnici: {len(clients)}")
        last_print = time.time()

    for key, _ in events:
        if key.fileobj == lsock:
            conn, addr = lsock.accept()
            conn.setblocking(False)
            sel.register(conn, selectors.EVENT_READ)
            clients[conn] = {"addr": addr, "name": None}

        else:
            conn = key.fileobj

            try:
                data = conn.recv(1024)
            except:
                data = None

            if data:
                message = data.decode().strip()

                if clients[conn]["name"] is None:
                    clients[conn]["name"] = message
                    print(f"[LOGIN] {message}")
                    log(f"[LOGIN] {message}")

                elif message == "/users":
                    users = ", ".join(
                        [clients[c]["name"] for c in clients if clients[c]["name"]]
                    )
                    conn.sendall(f"Online: {users}".encode())

                else:
                    msg = f"{clients[conn]['name']}: {message}"
                    print(msg)
                    log(msg)

                    for c in clients:
                        if c != conn:
                            c.sendall(msg.encode())

            else:
                print(f"[LOGOUT] {clients[conn]['name']}")
                log(f"[LOGOUT] {clients[conn]['name']}")

                sel.unregister(conn)
                conn.close()
                del clients[conn]