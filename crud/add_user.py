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
        
        # Yeni kullanıcı oluştur (ID olmadan)
        new_user = {
            "name": user.name,
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
        
        # Klasörün varlığını kontrol et
        os.makedirs(os.path.dirname("./user.json"), exist_ok=True)
        
        # JSON dosyasına yaz
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "user.json dosyası oluşturuldu ve ilk kullanıcı eklendi.",
            "user": new_user
        }
    except Exception as e:
        # Diğer hatalar
        return {
            "success": False,
            "message": f"Kullanıcı eklenirken hata oluştu: {str(e)}"
        }