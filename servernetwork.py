import socket 
import threading

class Server():
    def __init__(self, game_name, game_category):
        self.port = 7870
        self.clients = []
        self.game_name = game_name
        self.game_category = game_category
        self.stop_event = threading.Event()  # Event zum Stoppen der Schleife
    
    def waitConnection(self):
        # Auf Client-Anfragen warten
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))  # Lauscht auf alle IPs im lokalen Netz
        sock.settimeout(1)  # Timeout von 1 Sekunde
        
        print("Server hört wieder auf Broadcast-Anfragen...")
        
        while not self.stop_event.is_set():  # Überprüfen, ob das Stop-Event gesetzt wurde
            try:
                data, addr = sock.recvfrom(1024)
                if data.decode() == "DISCOVER_GAME":
                    print(f"Anfrage von {addr}, sende Antwort...")
                    sock.sendto(f"DISCOVER_ACK;{self.game_name};{self.game_category}".encode(), addr)

                elif data.decode() == "CONNECT_GAME":
                    print(f"Connect von {addr}, sende Antwort...")
                    self.clients.append(addr)
                    sock.sendto("CONNECT_ACK".encode(), addr)

            except socket.timeout:
                # Timeout erreicht, weiter prüfen, ob das Stop-Event gesetzt wurde
                continue
            except Exception as e:
                print(f"Fehler: {e}")
                break
        
        print("Server-Thread wird beendet.")
        sock.close()  # Socket schließen, wenn die Schleife beendet wird



# IP ermitteln
# host=socket.gethostbyname(socket.gethostname())

# # Socket erzeugen und mit Port verknuepfen
# UDPsocket = socket.socket(socket.AF_INET,    # Internet
#                          socket.SOCK_DGRAM)  # UDP-Protokoll
# UDPsocket.bind(('', port))

# # Ausgabe, damit die Clients die Verbindung aufbauen koennen

# print("Server ist an - PORT: "+str(port)+" - Adresse: "+host)

# nachricht=""
# while nachricht != "shutdown":

# # Empfangen einer Nachricht und Speicherung der Clientdaten (Adresse+Port):
#     data, addr = UDPsocket.recvfrom(1024)
# # Umwandlung des Bitstroms in Text:
#     nachricht=data.decode()
# # Ausgabe der Nachricht und der Clientadresse+Port 
#     print(nachricht + "von "+ str(addr[0])+ " : " + str(addr[1]))
   
# # Socket am Ende schliessen
# UDPsocket.close()
# print("Server shutdown from "+str(addr[0]))
