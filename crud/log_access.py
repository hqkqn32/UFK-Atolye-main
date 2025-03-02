import json
import os
import datetime
from typing import Dict, Optional

def log_access(user_rfid: str) -> Dict:
    
    try:
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        user = next((u for u in users if u.get("rfid_id") == user_rfid), None)
        
        if user is None:
            create_access_log(
                rfid_id=user_rfid,
                user_name=None,
                action="access_denied",
                success=False,
                message="Geçersiz RFID"
            )
            return {
                "success": False,
                "message": f"RFID: {user_rfid} ile eşleşen kullanıcı bulunamadı"
            }
        
        current_status = user.get("inside", False)
        new_status = not current_status  
        
        for u in users:
            if u.get("rfid_id") == user_rfid:
                u["inside"] = new_status
                break
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        action = "entry" if new_status else "exit"
        log_result = create_access_log(
            rfid_id=user_rfid,
            user_name=user.get("name"),
            action=action,
            success=True,
            message=f"Kullanıcı {'girişi' if new_status else 'çıkışı'} başarılı"
        )
        
        return {
            "success": True,
            "message": f"{user.get('name')} {'içeri girdi' if new_status else 'dışarı çıktı'}",
            "user": user,
            "log": log_result.get("log")
        }
        
    except Exception as e:
        create_access_log(
            rfid_id=user_rfid,
            user_name=None,
            action="error",
            success=False,
            message=str(e)
        )
        return {
            "success": False,
            "message": f"İşlem sırasında hata oluştu: {str(e)}"
        }

def create_access_log(rfid_id: str, user_name: Optional[str], action: str, success: bool, message: str) -> Dict:
    """
    Giriş-çıkış logu oluşturur
    
    Args:
        rfid_id (str): RFID kart ID'si
        user_name (str, optional): Kullanıcı adı, bulunamazsa None
        action (str): İşlem türü ('entry', 'exit', 'access_denied', 'error')
        success (bool): İşlem başarılı mı?
        message (str): İşlem mesajı
        
    Returns:
        dict: İşlem sonucu ve oluşturulan log
    """
    try:
        try:
            with open("log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        new_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "rfid_id": rfid_id,
            "user_name": user_name,
            "action": action,
            "success": success,
            "message": message
        }
        
        logs.append(new_log)
        
        with open("log.json", "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "message": "Log başarıyla oluşturuldu",
            "log": new_log
        }
    
    except Exception as e:
        print(f"Log oluşturulurken hata: {str(e)}")  
        return {
            "success": False,
            "message": f"Log oluşturulurken hata oluştu: {str(e)}"
        }

def get_all_logs() -> Dict:
    """
    Tüm giriş-çıkış loglarını getirir
    
    Returns:
        dict: İşlem sonucu ve loglar
    """
    try:
        with open("log.json", "r", encoding="utf-8") as file:
            logs = json.load(file)
        
        return {
            "success": True,
            "message": f"{len(logs)} log kaydı bulundu",
            "logs": logs
        }
    
    except FileNotFoundError:
        return {
            "success": False,
            "message": "log.json dosyası bulunamadı, henüz log kaydı oluşturulmamış"
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "log.json dosyası geçersiz JSON formatında"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Loglar getirilirken hata oluştu: {str(e)}"
        }