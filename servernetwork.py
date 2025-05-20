import socket 
import threading

class Server():
    def __init__(self, game_name, game_category, client_callback):
        self.port = 7870  # Port, auf dem der Server lauscht
        self.clients = []  # Liste der verbundenen Clients (IP, Port)
        self.game_name = game_name  # Name des Spiels (z. B. "TicTacToe")
        self.game_category = game_category  # Kategorie des Spiels (z. B. "Strategie")
        self.stop_event = threading.Event()  # Event-Objekt zum Stoppen der while-Schleife
        self.client_callback = client_callback  # Callback-Funktion, wenn ein Client sich verbindet oder verlässt
        
        # Erstelle UDP-Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))  # Lausche auf alle Netzwerkschnittstellen (0.0.0.0)
        self.sock.settimeout(1)  # Timeout von 1 Sekunde für recvfrom, damit Stop-Event geprüft werden kann
    
    def waitConnection(self):
        # Funktion zum Warten auf eingehende Verbindungen und Nachrichten
        
        sock = self.sock  # Verwende das Attribut
        
        print("Server hört wieder auf Broadcast-Anfragen...")
        
        # Solange das Stop-Event nicht gesetzt wurde
        while not self.stop_event.is_set():
            try:
                data, addr = sock.recvfrom(1024)  # Empfang von bis zu 1024 Bytes
                if data.decode() == "DISCOVER_GAME":
                    # Wenn ein Client das Spiel im Netzwerk sucht
                    print(f"Anfrage von {addr}, sende Antwort...")
                    sock.sendto(f"DISCOVER_ACK;{self.game_name};{self.game_category}".encode(), addr)

                elif data.decode() == "CONNECT_GAME":
                    # Wenn ein Client beitreten will
                    print(f"Connect von {addr}, sende Antwort...")
                    self.clients.append(addr)  # Client zur Liste hinzufügen
                    sock.sendto("CONNECT_ACK".encode(), addr)  # Bestätigung senden
                    # self.callNewPlayer(addr[0])  # Andere Clients über neuen Spieler informieren
                    self.client_callback("CONNECT_GAME", addr)  # Callback aufrufen
                
                elif data.decode() == "LEAVE_GAME":
                    # Wenn ein Client das Spiel verlassen möchte
                    print(f"Leave von {addr}, sende Antwort...")
                    self.clients.remove(addr)  # Client entfernen
                    sock.sendto("LEAVE_ACK".encode(), addr)  # Bestätigung senden
                    self.client_callback("LEAVE_GAME", addr)  # Callback aufrufen

                elif data.decode() == "RETRIEVE_PLAYERS":
                    # Wenn ein Client wissen möchte, wer spielt mit?
                    print(f"Retrieve von {addr}, sende Antwort...")
                    sock.sendto("RETRIEVE_ACK".encode(), addr)  # Bestätigung senden

                    data, addr = sock.recvfrom(1024)  # Erwartet START_RETRIEVE_PLAYERS
                    if data.decode() == "START_RETRIEVE_PLAYERS":
                        for client in self.clients:
                            sock.sendto(client[0].encode(), addr)  # Nur IP senden
                        sock.sendto("END_RETRIEVE_PLAYERS".encode(), addr)  # Ende signalisieren
                    

            except socket.timeout:
                # Timeout nach 1 Sekunde – prüfen, ob Schleife gestoppt werden soll
                continue
            except Exception as e:
                # Bei sonstigen Fehlern (z. B. Netzwerkfehler) abbrechen
                print(f"Fehler: {e}")
                break
        
        print("Server-Thread wird beendet.")
        sock.close()  # Socket schließen, wenn Server gestoppt wird
    
    def startGame(self):
        # Funktion zum Starten des Spiels – benachrichtigt alle Clients
        def handle_client(client):
            try:
                self.sock.sendto("START_GAME".encode(), client)
                self.sock.settimeout(5)
                data, addr = self.sock.recvfrom(1024)
                if data.decode() == "START_ACK":
                    print(f"START_ACK von {addr} erhalten.")
                else:
                    print(f"Unerwartete Antwort von {addr}: {data.decode()}")
            except socket.timeout:
                print(f"Timeout beim Warten auf START_ACK von {client}. \n Lösche Client")
                self.clients.remove(client)
            except Exception as e:
                print(f"Anderer Fehler im handle_client: {e}")
        for client in self.clients:
            threading.Thread(target=handle_client, args=(client,)).start()

    def callNewPlayer(self):
        # Funktion, um alle Clients über einen neuen Spieler zu informieren
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for client in self.clients:
            # Sende an alle Clients die neue Spieler-IP
            sock.sendto("NOTIFY_NEWPLAYER")



# (Alt-Code zum Empfangen einzelner Nachrichten – hier auskommentiert)

# host = socket.gethostbyname(socket.gethostname())

# UDPsocket = socket.socket(socket.AF_INET,    # Internet
#                          socket.SOCK_DGRAM)  # UDP-Protokoll
# UDPsocket.bind(('', port))

# print("Server ist an - PORT: "+str(port)+" - Adresse: "+host)

# nachricht=""
# while nachricht != "shutdown":
#     data, addr = UDPsocket.recvfrom(1024)
#     nachricht = data.decode()
#     print(nachricht + " von " + str(addr[0]) + " : " + str(addr[1]))
   
# UDPsocket.close()
# print("Server shutdown from "+str(addr[0]))
