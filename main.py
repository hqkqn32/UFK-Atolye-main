from fastapi import FastAPI
import json
import threading
import uvicorn
from crud.verify_admin import verify_user
from schemas import DoorOpenRequest,UserCreate
from crud.is_user import is_user
from crud.add_user import add_user_to_json



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "RFID Kontrol Sunucusu Çalışıyor"}
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  

server_thread.start()
print("FastAPI sunucusu çalışıyor")

@app.post("/open_Door")
async def open_door_from_admin(request:DoorOpenRequest):
    a=verify_user(request.username,request.password)

    return verify_user(request.username,request.password)
    

@app.post("/add_user")
async def add_user(request: UserCreate):
    result = add_user_to_json(request)
    return result


    return None

while True:
    a = input("ver: ")
    result = is_user(a)
    if result:
        print("Kullanıcı doğrulandı!")
    else:
        print("Kullanıcı bulunamadı!")





