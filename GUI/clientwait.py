# Importiere tkinter für GUI
import tkinter as tk
# Importiere threading für paralleles Ausführen (z. B. Server-Listener im Hintergrund)
import threading
# Importiere Netzwerkfunktionen für Client-Seite
from clientnetwork import listenServer, retrievePlayers, sock
import time
import socket



# Klasse für den "Warten auf Spielstart"-Bildschirm des Clients
class TriviaClientWait(tk.Frame):
    def __init__(self, parent, server_address):
        super().__init__(parent)
        self.start = False

        self.parent = parent

        self.sock = sock
        # Setze Fenstergröße
        self.parent.geometry("550x300")

        # Speichere die Serveradresse (z. B. IP + Port)
        self.server_address = server_address

        # Zurück-Button oben links
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Positioniere den Button oben links

        # Überschrift für die Spieleranzeige
        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()

        # Listbox zur Anzeige der verbundenen Clients
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        # Start-Button ist hier auskommentiert, da der Client nicht das Spiel startet
        # self.startButton = tk.Button(self, text="Spiel Starten", command=self.start_game)
        # self.startButton.pack(pady=10)
        self.searching = True
        self.wait_for_start = True
        threading.Thread(target=self.server_listen, daemon=True).start()  # Starte den Thread für die Serverkommunikation
        

    # Methode zum Hinzufügen eines Clients zur Listbox
    def add_client(self, client_address):
        self.server_listbox.insert(tk.END, f"Client: {client_address}")


    # Funktion, die im Thread läuft: Spieler abrufen und auf neue Spieler warten
    def server_listen(self):
        old_clients = []
        while self.searching and self.start == False:
            try:
                self.sock.settimeout(1)
                data, addr = self.sock.recvfrom(1024)
                msg = data.decode()
                if msg == "START_GAME":
                    self.start = True
                    self.sock.sendto("START_ACK".encode(), (self.server_address, 7870))
                    self.after(0, lambda: self.parent.show_game())
                elif msg == "NOTIFY_NEWPLAYER":
                    # Nur jetzt die Liste aktualisieren!
                    clients = retrievePlayers(self.server_address)
                    self.server_listbox.delete(0, tk.END)
                    for client in clients:
                        self.server_listbox.insert(tk.END, client)
            except socket.timeout:
                continue
                        
            if(old_clients == []):
                time.sleep(0.5)  # Wenn keine Spieler vorhanden sind, warte 0.5 Sekunden
            else:
                time.sleep(2)


    # Wenn der Zurück-Button gedrückt wird
    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Versucht, das Event zu setzen (Problem: self.game_server existiert hier nicht!)
        self.waitThread.join()  # Wartet auf das Ende des Threads
        self.parent.show_servercreate()  # Geht zurück zum Spiel-Erstellungs-Bildschirm
