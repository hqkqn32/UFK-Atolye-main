import json
from typing import Dict, List, Union

def get_inside_users() -> Dict[str, Union[bool, str, List]]:
    """
    İçeride olan (inside=true) kullanıcıları getirir
    
    Returns:
        dict: İşlem sonucu ve içerideki kullanıcı listesi
    """
    try:
        # user.json dosyasını oku
        with open("user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        # Inside değeri true olan kullanıcıları filtrele
        inside_users = [u for u in users if u.get("inside") == True]
        
        return {
            "success": True,
            "message": f"{len(inside_users)} kullanıcı içeride",
            "total_count": len(inside_users),
            "users": inside_users
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