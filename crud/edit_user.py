import json
import os
from schemas import UserEdit  # Kullanıcı düzenleme için şema

def edit_user_in_json(user_id: str, updated_data: UserEdit):
    try:
        # JSON dosyasını oku
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)

        user_index = next((i for i, u in enumerate(users) if u.get("id") == user_id or u.get("rfid_id") == user_id), None)
        
        if user_index is None:
            return {
                "success": False,
                "message": f"Kullanıcı bulunamadı (ID veya RFID: {user_id})"
            }
        
        # Mevcut kullanıcı verisini güncelle
        user = users[user_index]
        for key, value in updated_data.dict(exclude_unset=True).items():
            user[key] = value  # Sadece gönderilen alanları günceller
        
        # Güncellenmiş kullanıcıyı tekrar kaydet
        users[user_index] = user
        
        # JSON dosyasına yaz
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Kullanıcı başarıyla güncellendi.",
            "user": user
        }

    except FileNotFoundError:
        return {
            "success": False,
            "message": "user.json dosyası bulunamadı."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcı güncellenirken hata oluştu: {str(e)}"
        }
