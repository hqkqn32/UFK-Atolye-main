from fastapi import FastAPI
import json
import threading
import uvicorn

app = FastAPI()

def is_user(user_rfid):
    try:
        with open("user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
            
        user = next((u for u in users if u.get("rfid_id") == user_rfid), None)
        
        if user is None:
            return False
            
        return True
    except Exception as e:
        print(f"Hata: {str(e)}")
        return False

@app.get("/")
async def root():
    return {"message": "RFID Kontrol Sunucusu Çalışıyor"}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  

server_thread.start()
print("FastAPI sunucusu çalışıyor")

while True:
    a = input("ver: ")
    result = is_user(a)
    if result:
        print("Kullanıcı doğrulandı!")
    else:
        print("Kullanıcı bulunamadı!")

    