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

def connectToServer(adress):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("CONNECT_GAME".encode(),(adress,port))

    data, addr = sock.recvfrom(1024)
    if data.decode() == "CONNECT_ACK":
        print("Client Connected")


# host = input("Host:")
# # Socket erzeugen
# UDPsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
# nachricht=""
# while nachricht != "shutdown":
#   nachricht=input("Nachricht:")
# # Nachricht versenden
#   UDPsocket.sendto(nachricht.encode(),(host,port))
# UDPsocket.close()