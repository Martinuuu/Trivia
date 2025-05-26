import socket 
import threading
from trivia_api import Api
import json
import time

class Server():
    def __init__(self, game_name, game_category, client_callback):
        self.port = 7870  # Port, auf dem der Server lauscht
        self.clients = []  # Liste der verbundenen Clients (IP, Port)
        self.game_name = game_name  # Name des Spiels
        self.game_category = game_category  # Kategorie des Spiels (z. B. "Strategie")
        self.stop_event = threading.Event()  # Event-Objekt zum Stoppen der while-Schleife
        self.client_callback = client_callback  # Callback-Funktion, wenn ein Client sich verbindet oder verlässt
        self.client_names = {}  # addr -> Name des Clients (z. B. "Max Mustermann")
        self.api = Api()  # Instanz der API-Klasse erstellen (z. B. für Fragen)

        self.current_answers = {}  # addr -> Antwort
        self.scores = {}           # addr -> Punkte
        self.current_question_index = 0

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
                    
                    if addr in self.clients:
                        self.remove_player(addr)
                    
                    sock.sendto(f"DISCOVER_ACK;{self.game_name};{self.game_category}".encode(), addr)

                elif data.decode().startswith("CONNECT_GAME;"):
                    name = data.decode().split(";", 1)[1]
                    print(f"Connect von {addr} mit Name {name}, sende Antwort...")
                    self.clients.append(addr)
                    self.client_names[addr] = name  # Name speichern
                    sock.sendto("CONNECT_ACK".encode(), addr)
                    self.callNewPlayer()
                    self.client_callback("CONNECT_GAME", addr)
                
                elif data.decode() == "LEAVE_GAME":
                    print(f"Leave von {addr}, sende Antwort...")
                    self.remove_player(addr)

                elif data.decode() == "RETRIEVE_PLAYERS":
                    print(f"Retrieve von {addr}, sende Antwort...")
                    sock.sendto("RETRIEVE_ACK".encode(), addr)  # Bestätigung senden
                
                    data, addr = sock.recvfrom(1024)  # Erwartet START_RETRIEVE_PLAYERS
                    if data.decode() == "START_RETRIEVE_PLAYERS":
                        print(f"Starte Retrieve von {addr}, sende Spieler...")
                        for client in self.clients:
                            # Sende Name statt IP!
                            name = self.client_names.get(client, client[0])
                            sock.sendto(f"NAME;{name}".encode(), addr)
                            print(f"Sende Client: {name} an {addr}")
                        sock.sendto("END_RETRIEVE_PLAYERS".encode(), addr)  # Ende signalisieren
                        print(f"Ende Retrieve von {addr}, sende END_RETRIEVE_PLAYERS")
                
                
                # elif data.decode().startswith("ANSWER;"):
                #     answer = data.decode().split(";", 1)[1]
                #     print(f"Antwort von {addr}: {answer}")
                #     self.current_answers[addr] = answer

                #     # Punkte initialisieren, falls noch nicht vorhanden
                #     if addr not in self.scores:
                #         self.scores[addr] = 0

                #     # Wenn alle Clients geantwortet haben:
                #     if len(self.current_answers) == len(self.clients):
                #         self.evaluate_answers()
                #         self.current_answers = {}
                #         self.current_question_index += 1
                #         self.send_next_question()    

            except socket.timeout:
                # Timeout nach 1 Sekunde – prüfen, ob Schleife gestoppt werden soll
                continue
            except Exception as e:
                # Bei sonstigen Fehlern (z. B. Netzwerkfehler) abbrechen
                print(f"Fehler: {e}")
                break
        
        print("Server-Thread wird beendet.")
        sock.close()  # Socket schließen, wenn Server gestoppt wird

    def remove_player(self, addr):
        # Wenn ein Client das Spiel verlassen möchte
        print(f"Entferne {addr}")
        self.clients.remove(addr)  # Client entfernen
        self.sock.sendto("LEAVE_ACK".encode(), addr)  # Bestätigung senden
        self.client_callback("LEAVE_GAME", addr)  # Callback aufrufen
    
    def evaluate_answers(self):
        # Hole die richtige Antwort der aktuellen Frage
        frage = self.fragen[self.current_question_index]
        correct = frage["correct_answer"]
        print(f"Richtige Antwort: {correct}")

        # Punkte vergeben
        for addr, answer in self.current_answers.items():
            if answer == correct:
                self.scores[addr] += 1

        # Punkte an alle Clients schicken
        for client in self.clients:
            score = self.scores.get(client, 0)
            msg = f"SCORE;{score}"
            self.sock.sendto(msg.encode(), client)


    def startGame(self):
        fragen = self.api.get_trivia(self.game_category, amount=20)
        self.fragen = fragen

        # Sende START_GAME an alle Clients
        for client in self.clients:
            self.sock.sendto("START_GAME".encode(), client)

        received_acks = []
        expected_acks = set(self.clients)
        self.sock.settimeout(5)
        start_time = time.time()
        while expected_acks and (time.time() - start_time < 5):
            try:
                data, addr = self.sock.recvfrom(1024)
                print("Erwarte ACK von:", expected_acks)
                print("Bekommen von:", addr)
                if data.decode() == "START_ACK" and addr in expected_acks:
                    print(f"START_ACK von {addr} erhalten.")
                    received_acks.append(addr)
                    expected_acks.remove(addr)
                else:
                    print(f"Unerwartete Antwort von {addr}: {data.decode()}")
            except socket.timeout:
                # Timeout, aber wir prüfen, ob noch ACKs fehlen
                break

        # Entferne Clients, die kein ACK geschickt haben
        for client in list(expected_acks):
            print(f"Kein START_ACK von {client}. Entferne Client.")
            self.clients.remove(client)

        # Jetzt sind alle ACKs da, jetzt Fragen senden!
        self.send_questions()

        

    def callNewPlayer(self):
        # Funktion, um alle Clients über einen neuen Spieler zu informieren
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for client in self.clients:
            # Informiert alle Clients über neuen Spieler
            sock.sendto("NOTIFY_NEWPLAYER".encode(), client)
    
    def send_questions(self):
        print("Fragen, die gesendet werden:", self.fragen)
        fragen_json = json.dumps(self.fragen)
        for client in self.clients:
            print(f"Sende Fragen an {client}")
            self.sock.sendto(f"QUESTIONS;{fragen_json}".encode(), client)


    def send_next_question(self):
        # Wenn weniger als 10 Fragen übrig sind, hole 10 neue dazu
        if len(self.fragen) - self.current_question_index < 10:
            neue_fragen = self.api.get_trivia(self.game_category, amount=10)
            if neue_fragen:
                self.fragen.extend(neue_fragen)
            else:
                print("Keine neuen Fragen von der API erhalten.")
                # Optional: Spiel beenden oder Info an die Clients schicken

        # Prüfe, ob noch Fragen vorhanden sind
        if self.current_question_index >= len(self.fragen):
            print("Keine Fragen mehr verfügbar.")
            return

        frage = self.fragen[self.current_question_index]
        fragen_json = json.dumps([frage])
        for client in self.clients:
            self.sock.sendto(f"QUESTIONS;{fragen_json}".encode(), client)

        # Jetzt das GUI-Update für die neue Frage und Scores!
        if hasattr(self.client_callback, "__call__"):
            # Erzeuge ein dict: name -> score
            name_scores = {}
            for addr, score in self.scores.items():
                name = self.client_names.get(addr, f"{addr[0]}:{addr[1]}")
                name_scores[name] = score
            self.client_callback("UPDATE_GUI", frage, name_scores)