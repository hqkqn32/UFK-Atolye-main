import json
from typing import Dict, Union, List

def get_user_by_id(user_id: str) -> Dict[str, Union[bool, str, Dict, List]]:
    """
    ID'ye göre kullanıcı bilgilerini getirir
    
    Args:
        user_id (str): Aranacak kullanıcı ID'si
        
    Returns:
        dict: İşlem sonucu ve kullanıcı bilgileri
    """
    try:
        # ./user.json dosyasını oku
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        # ID'ye göre kullanıcıyı ara
        user = next((u for u in users if u.get("id") == user_id), None)
        
        if user is None:
            return {
                "success": False,
                "message": f"ID: {user_id} ile eşleşen kullanıcı bulunamadı",
                "total_count": 0,
                "users": []
            }
        
        # Kullanıcıyı liste içinde döndür (response_model uyumluluğu için)
        return {
            "success": True,
            "message": f"Kullanıcı bulundu: {user.get('name', 'İsimsiz')}",
            "total_count": 1,
            "users": [user]
        }
    
    except FileNotFoundError:
        return {
            "success": False,
            "message": "./user.json dosyası bulunamadı, henüz kullanıcı eklenmemiş",
            "total_count": 0,
            "users": []
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "./user.json dosyası geçersiz JSON formatında",
            "total_count": 0,
            "users": []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Kullanıcı aranırken hata oluştu: {str(e)}",
            "total_count": 0,
            "users": []
        }