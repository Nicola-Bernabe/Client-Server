# Descrizione di cosa fa
Questo progetto è costituito da 2 componenti:il server e il client. Ci sono le 2 cartelle con i vari file: 
- docker-compose.yml
- client:
  -  client_docker.py
  -  Dockerfile
- server:
  -  Dockerfile
  -  index.html
  -  server_docker.py

 
Come si può notare ci sono i files per far eseguire Docker;infatti il codice si può eseguire usando gli strumenti e i comandi corretti.Ciò verrà discusso nel paragrafo 'Come eseguire il progetto'.
Il server_docker.py usa FastApi che è un framework Web moderno e molto veloce , poi nel sito ufficiale si trova un esempio che utilizza la Websocket che è utilizzata per il collegamento con il client. Il client usa anch'esso la Websocket per il collegamento al server.


# Come eseguire il progetto
Per eseguire il progetto ci sono 2 metodi:
## Prima alternativa senza Docker
Bisogna avviare prima il server e poi il client con le guenti linee di codice:
- py server_docker.py    usando il terminale nella cartella del server
- py client_docker.py    usando il terminale nella cartella del client
- Vado alla pagina http://127.0.0.1:8000/ con un browser ,scelgo un numero per i campi e poi clicco sul bottone 'invia tutto'
Ps:bisogna installare tutte le librerie e anche python
## Seconda alternativa usando Docker
Usando il terminale all' esterno alle seguenti cartelle ,client e server,  bisogna digitare delle linee di codice.
- docker-compose build
- docker-compose up

In caso di problemi usare anche il codice :
- docker-compose restart      
Quest' ultimo codice serve per riavviare i 2 contenitori.
Docker è stato usato perchè è più comodo usare un solo terminale e anche per isolare questi processi dall' esterno.

# Scaricare le principali librerie
Per semplicità è utile usare delle linee di comando dal terminale e installare da lì le librerie usando una distribuzione Linux(es Ubuntu):
- pip install fastapi   
- pip install docker
- pip install docker-compose

Se si utilizasse Window per usare Docker bisognerebbe fare i seguenti passaggi:
- https://www.docker.com/products/docker-desktop    scarico la versione di window
- https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly   è un link utile nel caso docker volesse anche WSL: basta seguire questa guida per la configurazione

# Problemi e possibili soluzioni
Nel caso si usasse Window bisognerebbe avviare Docker Desktop e poi eseguire il progetto con il comando 'docker build'
Un altro problema è che l' host deve esssere 0.0.0.0 nel server quando viene avviato docker, questo perchè deve ascoltare tutte le interfacce.Prima abbiamo detto che docker isola i processi, quindi è necessario che si ascoltino tutti gli ip usando appunto 0.0.0.0

# Link utili
- https://www.youtube.com/watch?v=UIv6UyOIUAk     come usare Fast api con html
- https://asmen.icopy.site/awesome/awesome-fastapi/ codici client server con websocket
- https://www.youtube.com/watch?v=K8_eJlA-Iwg&list=PL41j7vkwrst4CA0PXCzCeZ05BcCNyj0rS&index=5   per le porte ecc...
- https://stackoverflow.com/questions/64156387/reduce-latency-in-asyncio
- https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
- https://stackoverflow.com/questions/2067042/disabling-an-html-button-while-waiting-for-a-result  per disabilitare bottone html


# Author

- Nicola Bernabè 192582
