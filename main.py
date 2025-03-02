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
   
@app.post("/delete_user")
async def delete_user(request:DeleteUserRequest):
    return delete_user_from_json(username=request.username)


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


