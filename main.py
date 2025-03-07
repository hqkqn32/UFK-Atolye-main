from fastapi import FastAPI, HTTPException, Path, Query
import threading
import uvicorn
import tkinter as tk
from tkinter import messagebox
from schemas import DoorOpenRequest, UserCreate, DeleteUserRequest, UserListResponse, UserEdit
from crud.verify_admin import verify_user
from crud.is_user import is_user
from crud.add_user import add_user_to_json
from crud.delete_user import delete_user_from_json
from crud.rfid_processor import process_rfid
from crud.get_all_users import get_all_users
from crud.get_inside_users import get_inside_users
from crud.get_users import get_user_by_id
from crud.gpio import gpio
from crud.edit_user import edit_user_in_json
from crud.get_logs import *
from crud.get_duration import *
import RPi.GPIO as GPIO
import time


# GPIO Modunu ve Pini Ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)  # Işık başlangıçta kapalı
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)  # Başlangıçta kapalı
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.LOW)  # Başlangıçta kapalı

# FastAPI başlat
app = FastAPI()

# CORS Middleware (Frontend API'yi çağırabilsin diye)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "RFID Kontrol Sunucusu Çalışıyor"}

# API Fonksiyonları
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
    return add_user_to_json(request)


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
async def edit_user_api(user_id: str, updated_data: UserEdit):
    return edit_user_in_json(user_id, updated_data)


@app.get("/users", response_model=UserListResponse)
async def get_users():
    result = get_all_users()
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.get("/users/{user_id}", response_model=UserListResponse)
async def get_user_by_id_api(user_id: str = Path(..., description="Aranacak kullanıcı ID'si")):
    result = get_user_by_id(user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.get("/users-inside")
async def get_inside_users_api():
    result = get_inside_users()
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.get("/get_logs")
async def get_logs():
    logs = await get_all_logs()
    return {"status": "success", "count": len(logs), "logs": logs}


@app.get("/get_logs/{user_id}")
async def get_logs_by_user(user_id: str = Path(..., description="Kullanıcı ID'si")):
    logs = await get_logs_by_user_id(user_id)
    return {"status": "success", "count": len(logs), "user_id": user_id, "logs": logs}


@app.get("/get_logs/{user_id}/{limit}")
async def get_logs_limited(user_id: str, limit: int):
    logs = await get_logs_by_user_id_limited(user_id, limit)
    return {"status": "success", "count": len(logs), "user_id": user_id, "limit": limit, "logs": logs}


@app.get("/calculate_duration")
async def get_all_durations(start_date: str = Query(None, description="Başlangıç tarihi (DD.MM.YYYY)")):
    durations = await calculate_duration(start_date=start_date)
    return {"status": "success", "count": len(durations), "durations": durations}


@app.get("/calculate_duration/{user_id}")
async def get_user_duration(user_id: str, start_date: str = Query(None)):
    durations = await calculate_duration(user_id=user_id, start_date=start_date)
    return {"status": "success", "user_id": user_id, "durations": durations}


# FastAPI Sunucusunu Arka Planda Çalıştırma
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  
server_thread.start()

# ------------------- Tkinter Arayüzü -------------------
class RFIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Giriş")
        self.root.geometry("400x200")

        self.label = tk.Label(root, text="RFID Kodunu Gir:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.focus()  # Program açıldığında imleç burada olsun

        self.button = tk.Button(root, text="Gönder", font=("Arial", 12), command=self.process_rfid)
        self.button.pack(pady=10)

    def process_rfid(self):
        rfid_code = self.entry.get().strip()
        if not rfid_code:
            messagebox.showwarning("Hata", "Lütfen bir RFID kodu girin!")
            return

        processed = process_rfid(rfid_code)
        
        if not processed:
            result = is_user(rfid_code)
            if result:
                messagebox.showinfo("Başarılı", "Kullanıcı doğrulandı!")
            else:
                messagebox.showerror("Hata", "Kullanıcı bulunamadı!")
        else:
            messagebox.showinfo("Bilgi", "RFID işlemi tamamlandı!")

        self.entry.delete(0, tk.END)  # Input alanını temizle


# Tkinter Arayüzünü Başlat
root = tk.Tk()
app = RFIDApp(root)
root.mainloop()
