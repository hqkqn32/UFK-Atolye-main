import json
from schemas import UserCreate
import os

def add_user_to_json(user: UserCreate):
    try:
        # JSON dosyasını oku
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        # Aynı RFID'ye sahip kullanıcı var mı kontrol et
        existing_user = next((u for u in users if u.get("rfid_id") == user.rfid_id), None)
        if existing_user:
            return {
                "success": False,
                "message": f"Bu RFID ({user.rfid_id}) zaten kullanımda."
            }
        

        max_id = 0
        for u in users:
            if "id" in u and u["id"].isdigit():
                id_num = int(u["id"])
                if id_num > max_id:
                    max_id = id_num
        
        # Yeni ID oluştur
        new_id = str(max_id + 1)
        
        # Yeni kullanıcı oluştur (ID olmadan)
        new_user = {
            "id":new_id,
            "name": user.name,
            "surname":user.surname,
            "rfid_id": user.rfid_id,
            "role": user.role,
            "inside": user.inside,
            "department": user.department,
            "mail": user.mail
        }
        
        # Kullanıcıyı listeye ekle
        users.append(new_user)
        
        # JSON dosyasına yaz
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": f"Kullanıcı başarıyla eklendi.",
            "user": new_user
        }
        
    except FileNotFoundError:
        # Dosya yoksa yeni bir liste oluştur
        users = []
        new_user = {
            "name": user.name,
            "rfid_id": user.rfid_id,
            "role": user.role,
            "inside": user.inside,
            "department": user.department,
            "mail": user.mail
        }


        
        users.append(new_user)
        
        os.makedirs(os.path.dirname("./user.json"), exist_ok=True)
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "user.json dosyası oluşturuldu ve ilk kullanıcı eklendi.",
            "user": new_user
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcı eklenirken hata oluştu: {str(e)}"
        }