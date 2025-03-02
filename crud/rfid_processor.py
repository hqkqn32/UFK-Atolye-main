import json
import datetime

def process_rfid(rfid_id):
    """
    RFID değerini işler, kullanıcı durumunu günceller ve log tutar
    
    Args:
        rfid_id (str): İşlenecek RFID değeri
        
    Returns:
        bool: Kullanıcı bulundu ise True, bulunamadı ise False
    """
    try:
        # ./././user.json dosyasından kullanıcıları oku
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        # RFID'ye göre kullanıcıyı bul
        user = None
        user_index = -1
        
        for i, u in enumerate(users):
            if u.get("rfid_id") == rfid_id:
                user = u
                user_index = i
                break
        
        # Kullanıcı bulunamadıysa False döndür
        if user is None:
            # Başarısız giriş deneyi için log tut
            log_access_attempt(rfid_id, None, "access_denied", False, "Geçersiz RFID")
            return False
        
        # Kullanıcı bulunduysa, inside durumunu tersine çevir
        current_status = user.get("inside", False)
        new_status = not current_status
        
        # ././user.json dosyasını güncelle
        users[user_index]["inside"] = new_status
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        # Başarılı giriş/çıkış için log tut
        action = "entry" if new_status else "exit"
        action_text = "girişi" if new_status else "çıkışı"
        
        log_access_attempt(
            rfid_id,
            user.get("name"),
            action, 
            True,
            f"Kullanıcı {action_text} başarılı"
        )
        
        # Ekstra bilgi yazdır
        print(f">> {user.get('name')} {'içeri girdi' if new_status else 'dışarı çıktı'}")
        print(f">> Durum: {'İçeride' if new_status else 'Dışarıda'}")
        
        return True
        
    except Exception as e:
        print(f">> HATA: {str(e)}")
        return False

def log_access_attempt(rfid_id, user_name, action, success, message):
    """
    Giriş-çıkış veya erişim deneyimini loglar
    
    Args:
        rfid_id (str): RFID değeri
        user_name (str): Kullanıcı adı (bulunamadıysa None)
        action (str): İşlem ("entry", "exit", "access_denied")
        success (bool): İşlem başarılı mı?
        message (str): Log mesajı
    """
    try:
        # ./log.json dosyasını oku, yoksa oluştur
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []
        
        # Şu anki zamanı al
        now = datetime.datetime.now()
        timestamp = now.isoformat()
        time_formatted = now.strftime("%d.%m.%Y %H:%M:%S")
        
        # Yeni log girdisi oluştur
        log_entry = {
            "timestamp": timestamp,
            "time": time_formatted,
            "rfid_id": rfid_id,
            "user_name": user_name,
            "action": action,
            "success": success,
            "message": message
        }
        
        # Log listesine ekle
        logs.append(log_entry)
        
        # Güncellenmiş log listesini dosyaya yaz
        with open("./log.json", "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f">> Log yazma hatası: {str(e)}")