#!/usr/bin/env python3



#r = requests.post("http://localhost:8000/")
#resp = req.get("http://localhost:8000/", params='n_messaggi')
#print('Status Code: ',r.status_code)
#print(resp.text)
#print("\n".join(['{} : {}'.format(name, type(getattr(requests,name))) for name in dir(requests)]))


import asyncio
import websockets
import time
import threading

async def spedire_messaggi():
    uri = "ws://127.0.0.1:8000/client"#uri per connettersi al server
    async with websockets.connect(uri) as websocket:#connessione al server
        
        th = threading.Thread(target=await threadFunc(websocket))
        th.start
async def threadFunc(websocket):
    manda_messaggi=False
    #differenza_tempo=[]
    while(1):
        variable=await websocket.recv()#ricevo i comandi dal server
        print(variable)
        if(variable=='latenza'):#se ho ricevuto il comando latenza dal server entro nel loop 
            manda_messaggi=True
            while manda_messaggi:
                await websocket.send(str(-2))
                variable=await websocket.recv()
                if(variable=='fine'):#se ricevo un comando chiamato 'fine' vol dire che esco dal loop della latenza
                    manda_messaggi=False
                    break
        if( variable=='throughput'):#ricevo dal server il comando 'throughput'
            manda_messaggi=True
            n_coppie=await  websocket.recv()#n coppie di messaggi 
            n_coppie=int(n_coppie)
            

            while manda_messaggi:
                variable1=await websocket.recv()
                variable2=await websocket.recv()
                await websocket.send(str(variable1))
                await  websocket.send(str(variable2))
                n_coppie-=1
                if(n_coppie==0):#ho finito le coppie di messaggi,esco dal loop
                    manda_messaggi=False
                  
                    break 
asyncio.get_event_loop().run_until_complete(spedire_messaggi())