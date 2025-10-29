from socket import *
import select

s = socket()
s.bind(("0.0.0.0", 2401))
s.listen()

clients = []

def connect_clients():
    client_is_waiting, _, _ = select.select([s], [], [], 0.0)
    if client_is_waiting:
        client, _ = s.accept()
        clients.append(client)

def on_receive_message(msg):
    for client in clients[:]:
        try:
            client.send(msg)
        except:
            clients.remove(client)
            client.close()

def update():
    connect_clients()

    for client in clients[:]:
        client_sent_message, _, _ = select.select([client], [], [], 0.0)
        if client_sent_message:
            server_msg = client.recv(1001)
            if not server_msg:
                clients.remove(client)
                client.close()
                continue

            on_receive_message(server_msg)

while True:
    update()