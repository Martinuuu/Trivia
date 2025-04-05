import socket 

# Standard Port festlegen
port = 7470
clients = []

def waitConnection():
    #Auf Client Anfragen warten
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))  # Lauscht auf alle IPs im lokalen Netz

    print("Server wartet auf Broadcast-Anfragen...")

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "DISCOVER_TRIVIA_GAME":
            print(f"Anfrage von {addr}, sende Antwort...")
            sock.sendto("SERVER_ACK".encode(), addr)



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
