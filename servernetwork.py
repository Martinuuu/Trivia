import socket 


class Server():
    def __init__(self, game_name, game_category):
        self.port = 7870
        self.clients = []
        self.game_name = game_name
        self.game_category = game_category
    def waitConnection(self):
        #Auf Client Anfragen warten
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))  # Lauscht auf alle IPs im lokalen Netz

        print("Server wartet auf Broadcast-Anfragen...")
        while True:
            data, addr = sock.recvfrom(1024)
            if data.decode() == "DISCOVER_GAME":
                print(f"Anfrage von {addr}, sende Antwort...")
                sock.sendto(f"DISCOVER_ACK;{self.game_name};{self.game_category}".encode(), addr)
            
            if data.decode() == "CONNECT_GAME":
                print(f"Connect von {addr}, sende Antwort...")
                self.clients.append(addr)
                sock.sendto("CONNECT_ACK".encode(), addr)



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
