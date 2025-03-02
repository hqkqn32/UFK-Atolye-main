import json
from typing import Dict, List, Union

def get_all_users() -> Dict[str, Union[bool, str, List]]:
    try:
        # user.json dosyasını oku
        with open("user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        return {
            "success": True,
            "message": f"{len(users)} kullanıcı bulundu",
            "total_count": len(users),
            "users": users
        }
    
    except FileNotFoundError:
        return {
            "success": False,
            "message": "user.json dosyası bulunamadı, henüz kullanıcı eklenmemiş",
            "total_count": 0,
            "users": []
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "user.json dosyası geçersiz JSON formatında",
            "total_count": 0,
            "users": []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcılar getirilirken hata oluştu: {str(e)}",
            "total_count": 0,
            "users": []
        }
    
