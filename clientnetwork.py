import socket

# Erfragen von Port und Host des Servers (der muss zuerst gestartet werden!)
port = 7870


def checkServer():
    server_list = []
    broadcast_address = '<broadcast>'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET,UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)  # 2 Sekunden warten auf Antwort

    # Broadcast senden
    sock.sendto("DISCOVER_GAME".encode(), (broadcast_address, port))

    try:
        data, addr = sock.recvfrom(1024)
        data = data.decode().split(";")
        print(f"Antwort von Server: {data[0]} von {addr}")
        if data[0] == "DISCOVER_ACK":
            server_list.append(f"{data[1]} - {data[2]}: {addr[0]}")
    except socket.timeout:
        print("Kein Server gefunden.")
    return server_list

def connectToGame(adress):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("CONNECT_GAME".encode(),(adress,port))

    data, addr = sock.recvfrom(1024)
    if data.decode() == "CONNECT_ACK":
        print("Client Connected")
        return True

def leaveGame(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("LEAVE_GAME".encode(),(address,port))

    data, addr = sock.recvfrom(1024)
    if data.decode() == "LEAVE_ACK":
        print("Client hat das Spiel verlassen")

def retrievePlayers(address):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("RETRIEVE_PLAYERS".encode(),(address,port))
    print("Retrieve gesendet")
    data, addr = sock.recvfrom(1024)
    print(data.decode())
    if data.decode() == "RETRIEVE_ACK":
        print("Retrieve Ack bekommen")
        clients = []
        sock.sendto("START_RETRIEVE_PLAYERS".encode(),(address,port))
        data = "".encode()
        while data.decode() != "END_RETRIEVE_PLAYERS":
            data, addr = sock.recvfrom(1024)
            clients.append(data.decode())
        return clients

def listenServer(server_address, update_client_list_callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET,UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)  # 2 Sekunden warten auf Antwort

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if addr[0] == server_address:
                print(f"Nachricht von {server_address}: {data.decode()}")
                if data.decode() == "START_GAME":
                    sock.sendto("START_ACK".encode(), (server_address, port))
                if "RECIEVE_CLIENT" in data.decode():
                    client = data.decode().split(";")[1]
                    update_client_list_callback(client)
                    #sock.sendto("RECIEVE_ACK".encode(), (server_address, port))
    except socket.timeout:
        pass  # Continue looping on timeout

# host = input("Host:")
# # Socket erzeugen
# UDPsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
# nachricht=""
# while nachricht != "shutdown":
#   nachricht=input("Nachricht:")
# # Nachricht versenden
#   UDPsocket.sendto(nachricht.encode(),(host,port))
# UDPsocket.close()