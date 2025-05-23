import socket
import random
import time
# Erfragen von Port und Host des Servers (der muss zuerst gestartet werden!)
server_port = 7870
client_port = random.randint(10000, 60000)
print("Starte Client mit Port: " + str(client_port))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', client_port))

def checkServer():
    server_list = []
    broadcast_address = '<broadcast>'

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET,UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)  # 2 Sekunden warten auf Antwort

    # Broadcast senden
    sock.sendto("DISCOVER_GAME".encode(), (broadcast_address, server_port))

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
    # sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("CONNECT_GAME".encode(),(adress,server_port))

    data, addr = sock.recvfrom(1024)
    if data.decode() == "CONNECT_ACK":
        print("Client Connected")
        return True

def leaveGame(address):
    # sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    sock.sendto("LEAVE_GAME".encode(),(address,server_port))

    data, addr = sock.recvfrom(1024)
    if data.decode() == "LEAVE_ACK":
        print("Client hat das Spiel verlassen")

def retrievePlayers(address):
    # sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    try:    
        sock.sendto("RETRIEVE_PLAYERS".encode(),(address,server_port))
        print("Retrieve gesendet")
        data, addr = sock.recvfrom(1024)
        if data.decode() == "START_GAME":
            return ["START_GAME"]
        print(data.decode())
        if data.decode() == "RETRIEVE_ACK":
            print("Retrieve Ack bekommen")
            clients = []
            sock.sendto("START_RETRIEVE_PLAYERS".encode(),(address,server_port))
            data = "".encode()
            while data.decode() != "END_RETRIEVE_PLAYERS":
                data, addr = sock.recvfrom(1024)
                clients.append(data.decode())
            clients.pop(-1) # Löscht den letzten Eintrag (END_RETRIEVE_PLAYERS)
            return clients
        else:
            return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Clients: {e}")
        return []


def listenServer(server_address, gui_callback, server_listbox):
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET,UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)  # 2 Sekunden warten auf Antwort
    start = False
    old_clients = []
    while start == False:
        try:
            data, addr = sock.recvfrom(65536)
            msg = data.decode()
            if msg == "START_GAME":
                print("START_GAME empfangen, sende START_ACK an", server_address)
                start = True
                sock.sendto("START_ACK".encode(), (server_address, 7870))
                gui_callback()
                # self.after(0, lambda: self.parent.show_game([]))
            if msg == "NOTIFY_NEWPLAYER":
                # Nur jetzt die Liste aktualisieren!
                clients = retrievePlayers(server_address)
                server_listbox.delete(0, "end")
                for client in clients:
                    server_listbox.insert("end", client)
        except socket.timeout:
            continue
                        
        if(old_clients == []):
            time.sleep(0.5)  # Wenn keine Spieler vorhanden sind, warte 0.5 Sekunden
        else:
            time.sleep(2)
# host = input("Host:")
# # Socket erzeugen
# UDPsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
# nachricht=""
# while nachricht != "shutdown":
#   nachricht=input("Nachricht:")
# # Nachricht versenden
#   UDPsocket.sendto(nachricht.encode(),(host,port))
# UDPsocket.close()