# crud/logs.py
import json

async def get_all_logs():
    """
    Tüm log kayıtlarını getirir.
    
    Returns:
        list: Tüm log kayıtları
    """
    try:
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Logları son kayıttan ilk kayda doğru sırala (en yeni en üstte)
        logs.sort(key=lambda log: log.get("timestamp", ""), reverse=True)
        
        return logs
        
    except Exception as e:
        print(f">> Log okuma hatası: {str(e)}")
        return []

async def get_logs_by_user_id(user_id):
    """
    Belirli bir kullanıcıya ait log kayıtlarını getirir.
    
    Args:
        user_id (str): Kullanıcı ID'si
        
    Returns:
        list: Kullanıcıya ait log kayıtları
    """
    try:
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Kullanıcı ID'sine göre filtrele
        logs = [log for log in logs if log.get("user_id") == str(user_id)]
        
        # Logları son kayıttan ilk kayda doğru sırala (en yeni en üstte)
        logs.sort(key=lambda log: log.get("timestamp", ""), reverse=True)
        
        return logs
        
    except Exception as e:
        print(f">> Log okuma hatası: {str(e)}")
        return []

async def get_logs_by_user_id_limited(user_id, limit):
    """
    Belirli bir kullanıcıya ait belirli sayıdaki log kayıtlarını getirir.
    
    Args:
        user_id (str): Kullanıcı ID'si
        limit (int): Gösterilecek log sayısı
        
    Returns:
        list: Kullanıcıya ait belirli sayıdaki log kayıtları
    """
    try:
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Kullanıcı ID'sine göre filtrele
        logs = [log for log in logs if log.get("user_id") == str(user_id)]
        
        # Logları son kayıttan ilk kayda doğru sırala (en yeni en üstte)
        logs.sort(key=lambda log: log.get("timestamp", ""), reverse=True)
        
        # Belirtilen sayıda log döndür
        try:
            limit = int(limit)
            logs = logs[:limit]
        except (ValueError, TypeError):
            # Limit sayı değilse yoksay
            pass
        
        return logs
        
    except Exception as e:
        print(f">> Log okuma hatası: {str(e)}")
        return []