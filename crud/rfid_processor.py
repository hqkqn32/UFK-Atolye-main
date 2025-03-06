import json
import datetime
from .gpio import gpio
from .get_inside_users import get_inside_users



def process_rfid(rfid_id):
   
    try:
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        user = None
        user_index = -1
        
        for i, u in enumerate(users):
            if u.get("rfid_id") == rfid_id:
                user = u
                user_index = i
                break
        
        if user is None:
            log_access_attempt(rfid_id, None, "access_denied", False, "Geçersiz RFID")
            return False
        
        current_status = user.get("inside", False)
        new_status = not current_status
        
        users[user_index]["inside"] = new_status
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        action = "entry" if new_status else "exit"
        action_text = "girişi" if new_status else "çıkışı"
        
        log_access_attempt(
            rfid_id,
            user.get("name"),
            action, 
            True,
            f"Kullanıcı {action_text} başarılı"
        )
        
        print(f">> {user.get('name')} {'içeri girdi' if new_status else 'dışarı çıktı'}")
        print(f">> Durum: {'İçeride' if new_status else 'Dışarıda'}")

        gpio(27,"opendoor")

        inside_data = get_inside_users()
        inside_count = inside_data["total_count"]
        
        print(f">> İçerideki kişi sayısı: {inside_count}")

        if inside_count > 0:
            gpio(23, "light_on")  # Işıkları aç
            print(">> Işıklar açıldı!")
        else:
            gpio(23, "light_off")  # Işıkları kapat
            print(">> Işıklar kapatıldı!")
        
        return True
        
    except Exception as e:
        print(f">> HATA: {str(e)}")
        return False

def log_access_attempt(rfid_id, name, action, success, message):
 
    try:
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        now = datetime.datetime.now()
        timestamp = now.isoformat()
        time_formatted = now.strftime("%d.%m.%Y %H:%M:%S")
        
        log_entry = {
            "timestamp": timestamp,
            "time": time_formatted,
            "rfid_id": rfid_id,
            "name": name,
            "action": action,
            "success": success,
            "message": message
        }
        
        logs.append(log_entry)
        
        with open("./log.json", "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f">> Log yazma hatası: {str(e)}")