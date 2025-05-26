import socket
import random
import time
import json
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
        else: 
            checkServer()
            time.sleep(1)
    except socket.timeout:
        print("Kein Server gefunden.")
    return server_list

def connectToGame(address, name):
    # Sende Name mit
    msg = f"CONNECT_GAME;{name}"
    sock.sendto(msg.encode(), (address, server_port) if isinstance(address, str) else address)

    data, addr = sock.recvfrom(1024)
    if data.decode() == "CONNECT_ACK":
        print("Client Connected")
        return True

def leaveGame(address):
    sock.sendto("LEAVE_GAME".encode(), (address, server_port) if isinstance(address, str) else address)
    data, addr = sock.recvfrom(1024)
    if data.decode() == "LEAVE_ACK":
        print("Client hat das Spiel verlassen")

def retrievePlayers(address):
    try:    
        sock.sendto("RETRIEVE_PLAYERS".encode(), (address, server_port) if isinstance(address, str) else address)
        print("Retrieve gesendet")
        data, addr = sock.recvfrom(1024)
        if data.decode() == "START_GAME":
            return ["START_GAME"]
        print(data.decode())
        if data.decode() == "RETRIEVE_ACK":
            print("Retrieve Ack bekommen")
            clients = []
            sock.sendto("START_RETRIEVE_PLAYERS".encode(), (address, server_port) if isinstance(address, str) else address)
            data = "".encode()
            while "END_RETRIEVE_PLAYERS" not in data.decode():
                data, addr = sock.recvfrom(1024)
                clients.append(data.decode())
                print(f"Client: {data.decode()} von {addr}")
            print("Retrieve abgeschlossen")
            clients.pop(-1) # Löscht den letzten Eintrag (END_RETRIEVE_PLAYERS)
            return clients
        else:
            return []
    except Exception as e:
        print(f"Fehler beim Abrufen der Clients: {e}")
        return []


def listenServer(server_address, gui_callback, server_listbox, stop_event=None):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)
    start = False
    while not (stop_event and stop_event.is_set()) and start == False:
        try:
            data, addr = sock.recvfrom(65536)
            msg = data.decode()
            if msg == "START_GAME":
                print("START_GAME empfangen, sende START_ACK an", server_address)
                sock.sendto("START_ACK".encode(), server_address)
            if msg == "NOTIFY_NEWPLAYER":
                clients = retrievePlayers(server_address)
                if server_listbox.winfo_exists():
                    server_listbox.delete(0, "end")
                    for client in clients:
                        server_listbox.insert("end", client)
            if msg.startswith("QUESTIONS;"):
                print("Fragen empfangen:", msg)
                fragen_json = msg[len("QUESTIONS;"):]
                fragen = json.loads(fragen_json)
                gui_callback(fragen)  # Übergib die Fragen an das GUI
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Fehler im listenServer: {e}")
            break

def send_answer(server_address, answer):
    msg = f"ANSWER;{answer}"
    sock.sendto(msg.encode(), server_address)