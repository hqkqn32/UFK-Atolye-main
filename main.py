from fastapi import FastAPI, HTTPException, Path, Query
import json
import threading
import uvicorn
from crud.verify_admin import verify_user
from schemas import DoorOpenRequest, UserCreate, DeleteUserRequest, UserListResponse, UserEdit
from crud.is_user import is_user
from crud.add_user import add_user_to_json
from crud.delete_user import delete_user_from_json
from crud.rfid_processor import process_rfid
from crud.get_all_users import get_all_users
from crud.get_inside_users import get_inside_users
from crud.get_users import get_user_by_id
from fastapi.middleware.cors import CORSMiddleware
from crud.gpio import gpio
from crud.edit_user import edit_user_in_json
import RPi.GPIO as GPIO
import time
from crud.get_logs import *
from crud.get_duration import *
import keyboard  # Klavye girişini dinlemek için gerekli modül

# GPIO Modunu ve Pini Ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)  # Işık başlangıçta kapalı

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)  # Başlangıçta kapalı

GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)  # Başlangıçta kapalı

# FastAPI uygulamasını başlat
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend'in adresi
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metotlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)


@app.get("/")
async def root():
    return {"message": "RFID Kontrol Sunucusu Çalışıyor"}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  # Sunucu thread'i daemon olarak çalışacak

server_thread.start()
print("FastAPI sunucusu çalışıyor")

@app.post("/open_Door")
async def open_door_from_admin(request: DoorOpenRequest):
    if verify_user(request.username, request.password):
        gpio(27, "opendoor")
        return {"message": "Kapı 2 saniyeliğine açıldı!"}
    return {"error": "Yetkisiz erişim!"}

@app.post("/open_light")
async def open_light_admin(request: DoorOpenRequest):
    if verify_user(request.username, request.password):
        gpio(22, "light")
        return {"message": "Işık durumu değiştirildi"}
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

@app.put("/edit_user/{user_id}")
async def edit_user_in_json(user_id: str, updated_data: UserEdit):
    return edit_user_in_json(user_id, updated_data)

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

@app.get("/get_logs")
async def get_logs():
    logs = await get_all_logs()
    return {
        "status": "success",
        "count": len(logs),
        "logs": logs
    }

@app.get("/get_logs/{user_id}")
async def get_logs_by_user(user_id: str = Path(..., description="Kullanıcı ID'si")):
    logs = await get_logs_by_user_id(user_id)
    return {
        "status": "success",
        "count": len(logs),
        "user_id": user_id,
        "logs": logs
    }

@app.get("/get_logs/{user_id}/{limit}")
async def get_logs_limited(
    user_id: str = Path(..., description="Kullanıcı ID'si"),
    limit: int = Path(..., description="Gösterilecek log sayısı")
):
    logs = await get_logs_by_user_id_limited(user_id, limit)
    return {
        "status": "success",
        "count": len(logs),
        "user_id": user_id,
        "limit": limit,
        "logs": logs
    } 

@app.get("/calculate_duration")
async def get_all_durations(start_date: str = Query(None, description="Başlangıç tarihi (DD.MM.YYYY)")):
    durations = await calculate_duration(start_date=start_date)
    return {
        "status": "success",
        "count": len(durations),
        "durations": durations
    }

@app.get("/calculate_duration/{user_id}")
async def get_user_duration(
    user_id: str = Path(..., description="Kullanıcı ID'si"),
    start_date: str = Query(None, description="Başlangıç tarihi (DD.MM.YYYY)")
):
    durations = await calculate_duration(user_id=user_id, start_date=start_date)
    return {
        "status": "success",
        "user_id": user_id,
        "durations": durations
    }

# Klavye girişini dinleyerek RFID kart verisini alma
def listen_for_rfid():
    print("RFID kartını okutun...")
    while True:
        # 'enter' tuşuna basıldığında RFID verisini al
        if keyboard.is_pressed("enter"):
            rfid_value = ''.join(keyboard.get_typed_strings(keyboard.record(until='enter')))
            print(f"Okunan RFID: {rfid_value}")
            
            # RFID'yi işlemden geçir
            processed = process_rfid(rfid_value)
            if not processed:
                result = is_user(rfid_value)
                if result:
                    print("Kullanıcı doğrulandı!")
                else:
                    print("Kullanıcı bulunamadı!")
            time.sleep(1)  # 1 saniye bekleyip tekrar dinlemeye başla

# RFID dinleyicisini bir thread'de çalıştır
rfid_thread = threading.Thread(target=listen_for_rfid)
rfid_thread.daemon = True  # Thread'lerin ana işlemle birlikte kapanması için daemon

rfid_thread.start()
print("RFID dinleyici çalışıyor...")
