import socket

# Erfragen von Port und Host des Servers (der muss zuerst gestartet werden!)
port = 7470

def checkServer():
    broadcast_address = '<broadcast>'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)  # 2 Sekunden warten auf Antwort

    # Broadcast senden
    sock.sendto("DISCOVER_SERVER".encode(), (broadcast_address, port))

    try:
        data, addr = sock.recvfrom(1024)
        print(f"Antwort von Server: {data.decode()} von {addr}")
    except socket.timeout:
        print("Kein Server gefunden.")

checkServer()

# host = input("Host:")
# # Socket erzeugen
# UDPsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # INTERNET,UDP
# nachricht=""
# while nachricht != "shutdown":
#   nachricht=input("Nachricht:")
# # Nachricht versenden
#   UDPsocket.sendto(nachricht.encode(),(host,port))
# UDPsocket.close()