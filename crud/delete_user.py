import json
import os

def delete_user_from_json(username):
   
    try:
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        user_index = None
        user_to_delete = None
        
        for i, user in enumerate(users):
            if user.get("name") == username:
                user_index = i
                user_to_delete = user
                break
        
        if user_index is None:
            return {
                "success": False,
                "message": f"'{username}' adlı kullanıcı bulunamadı."
            }
        
        deleted_user = users.pop(user_index)
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": f"'{username}' adlı kullanıcı başarıyla silindi.",
            "deleted_user": deleted_user
        }
        
    except FileNotFoundError:
        return {
            "success": False,
            "message": "user.json dosyası bulunamadı."
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "user.json dosyası geçersiz JSON formatında."
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcı silinirken hata oluştu: {str(e)}"
        }

