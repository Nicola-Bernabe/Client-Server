#!/usr/bin/env python3
#link usati durante il progetto
#https://www.youtube.com/watch?v=UIv6UyOIUAk
#https://fastapi.tiangolo.com/deployment/docker/  #per aggiornare e passare parametri server-html
#http://127.0.0.1:8000/docs  vedere documentazione fast api del proprio progetto
#https://asmen.icopy.site/awesome/awesome-fastapi/ codici client server con websocket
#https://www.youtube.com/watch?v=K8_eJlA-Iwg&list=PL41j7vkwrst4CA0PXCzCeZ05BcCNyj0rS&index=5   per le porte ecc...
#https://stackoverflow.com/questions/64156387/reduce-latency-in-asyncio
#https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
#https://stackoverflow.com/questions/2067042/disabling-an-html-button-while-waiting-for-a-result  per disabilitare bottone

#uvicorn server_docker:app --reload
#http://127.0.0.1:8000/  


import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket
import threading
from fastapi.responses import HTMLResponse
import time
from numpy import byte, mean
from fastapi.responses import FileResponse
app = FastAPI()
template = Jinja2Templates(directory="./")
@app.get('/')#carito la pagina html
async def index():
    return FileResponse("index.html")

dati_precedenti=[1000,1]#così ho le variabili per mandare e ricevere messaggi client server,l'ordine è [nmessaggi,latenza]
dati_correnti=[False,10,1000,0,0,0,0]#blocco/sblocco,n_byte,n_messaggi_coppie,media throughput,media tempo aspettare 2 messaggio,tempo per throughput,tempo tot prima parte

@app.post("/", response_class=HTMLResponse)#serve per configurare il post del bottone
async def numero(request: Request,n_messaggi: int=Form(...),n_byte:int=Form(...),n_messaggi_coppie:int=Form(...)):
    
    dati_correnti[0]=True#serve per sbloccare il calcolo del tempo e dei messaggi da mandare al client
    dati_correnti[1]=n_byte#aggiorno valori in questa lista
    dati_correnti[2]=n_messaggi_coppie
    dati_precedenti[0]=n_messaggi
    while(dati_correnti[0]):#aspetto finchè finisce i calcoli della latenza
        await asyncio.sleep(0.2)#aspetto
    return template.TemplateResponse("index.html", {"request": request, "n_messaggi_stampo": dati_precedenti[0],'latenza':round(dati_precedenti[1],7),'t_totale':dati_correnti[6],'n_messaggi_coppie22':dati_correnti[2],'byte_messaggio':dati_correnti[1],'throughput1':round(dati_correnti[3]/1000000,7),'media_tempo_2_messaggio':round(dati_correnti[4],7),'t_thrughput':dati_correnti[5]})

@app.websocket("/client")#collegamento al client
async def websocket_endpoint(websocket: WebSocket):
    th = threading.Thread(target=await threadFunc(websocket))#creo un thread
    th.start
async def threadFunc(websocket):
    await websocket.accept()#accetto connessione
    while(1):
        condizione=dati_correnti[0]
        if(condizione):    #se ho fatto post posso entrare con questa condizione
            await websocket.send_text('latenza')
            data = await websocket.receive_text()
            await websocket.send_text('latenza')
            differenza_tempo=[]
            for i in range(int(dati_precedenti[0])):
                toc = time.perf_counter()
                await websocket.send_text(str(dati_precedenti[0]))
                risp = await websocket.receive_text()
                tic = time.perf_counter()
                differenza_tempo.append(tic-toc)
                await asyncio.sleep(0.001)#così si può aggiornare e non si crea congestione
            dati_correnti[6]=round(sum(differenza_tempo),5)
            m=mean(differenza_tempo)#media latenza
            dati_precedenti[1]=m
            await websocket.send_text('fine')

            #ora calcolo throughput
            #mi occupo dei byte da mandare
            testo_stringa=''
            testo_messaggio_byte=byte()
            for by in range(dati_correnti[1]):#creo grandezza della stringa, un carattere 'a' è un byte
                 testo_stringa+='a'
            testo_messaggio_byte=bytes(testo_stringa,'utf-8')
            #print('testo_messaggio_byte:  ',testo_messaggio_byte,len(testo_messaggio_byte))
            await websocket.send_text(str('throughput'))
            #risp =await websocket.receive_text()
            await websocket.send_text(str(dati_correnti[2]))
            differenza_tempo=[]
            t_inizio = time.perf_counter()#lo uso per capire quanto ci mette per calcolare il throughput
            variable2=await websocket.receive_text()
            for ii in range(dati_correnti[2]):#mando ii coppie di messaggi, uso un cronometro per tener conto del tempo 
                toc = time.perf_counter()
                await websocket.send_text(str(testo_messaggio_byte))
                await websocket.send_text(str(testo_messaggio_byte))
                variable1=await websocket.receive_text()
                variable2=await websocket.receive_text()
                tic = time.perf_counter()
                differenza_tempo.append(tic-toc)
                await asyncio.sleep(0.01)
            t_fine = time.perf_counter()#lo uso per capire quanto ci mette per calcolare il throughput
            m=mean(differenza_tempo)
            dati_correnti[4]=m
            m=(dati_correnti[1]*8*2)/m #bit/tempo, da byte a bit(*8 perchè 1 byte sono 8 bit),poi *2 perchè la dimensione dei dati trasmessi sono 2 pacchetti
            m=round(m,4)
            dati_correnti[3]=m
            dati_correnti[5]=round(t_fine-t_inizio,4)
            dati_correnti[0]=False#esco dal loop del post
            print('calcolato tutto')
        else:
            await asyncio.sleep(0.01)#non ho fatto post quindi aspetto