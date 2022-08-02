'''
    Elaborato Programmazione di Reti
            a.a. 2021/2022
            Mazzotti Giada
           Matricola: 802811
               Traccia 3
     Web Server Agenzia di Viaggi
'''

#!/bin/env python
import sys, signal
import http.server
import socketserver
#new imports
import threading 

#manage the wait witout busy waiting
waiting_refresh = threading.Event()

# primi articoli di ogni testata
first_articles = [] 

# Legge il numero della porta dalla riga di comando, e mette default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)


# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main():

    #Assicura che da tastiera usando la combinazione
    #di tasti Ctrl-C termini in modo pulito tutti i thread generati
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non è stato
    #rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler)
    #creo pagina recensioni

    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequestsGET.txt','w', encoding="utf-8")
    f.close()
    # entra nel loop infinito
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    server.server_close()

if __name__ == "__main__":
    main()
