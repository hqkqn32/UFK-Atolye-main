from fastapi import FastAPI, HTTPException, Path
import json
import threading
import uvicorn
from crud.verify_admin import verify_user
from schemas import DoorOpenRequest,UserCreate,DeleteUserRequest,UserListResponse
from crud.is_user import is_user
from crud.add_user import add_user_to_json
from crud.delete_user import delete_user_from_json
from crud.rfid_processor import process_rfid
from crud.get_all_users import get_all_users
from crud.get_inside_users import get_inside_users
from crud.get_users import get_user_by_id
from fastapi.middleware.cors import CORSMiddleware
import RPi.GPIO as GPIO
import time


# GPIO Pin Tanımları
DOOR_CONTROL_PIN = 27

# GPIO Modunu ve Pini Ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_CONTROL_PIN, GPIO.OUT)
GPIO.output(DOOR_CONTROL_PIN, GPIO.LOW)  # Başlangıçta kapalı

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend'in adresi
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metotlarını (GET, POST, PUT, DELETE) izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)


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
    if verify_user(request.username,request.password):
        GPIO.output(DOOR_CONTROL_PIN, GPIO.HIGH)  # Kapıyı aç
        time.sleep(4)  # 4 saniye bekle
        GPIO.output(DOOR_CONTROL_PIN, GPIO.LOW)  # Kapıyı kapat
        return {"message": "Kapı 4 saniyeliğine açıldı!"}
    
    return {"error": "Yetkisiz erişim!"}
    

@app.post("/add_user")
async def add_user(request: UserCreate):
    result = add_user_to_json(request)
    return result
   
@app.post("/delete_user")
async def delete_user(request: DeleteUserRequest):
    if not request.id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    result = delete_user_from_json(request.id)
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=500, detail=result["message"])


@app.get("/users", response_model=UserListResponse)
async def get_users():
    result = get_all_users()
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

@app.get("/users/{user_id}", response_model=UserListResponse)
async def get_user_by_id(user_id: str = Path(..., description="Aranacak kullanıcı ID'si")):
    """
    ID'ye göre kullanıcı bilgilerini getir
    """
    from crud.get_users import get_user_by_id  # İlgili import
    
    # await kaldırıldı
    result = get_user_by_id(user_id)
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


@app.get("/users-inside")
async def get_Inside():
    result = get_inside_users()

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result


while True:
    a = input("ver: ")
    
    processed = process_rfid(a)
    
    # Eğer işlenemediyse (geçersiz RFID), normal kullanıcı kontrolü yap
    if not processed:
        result = is_user(a)
        if result:
            print("Kullanıcı doğrulandı!")
        else:
            print("Kullanıcı bulunamadı!")


