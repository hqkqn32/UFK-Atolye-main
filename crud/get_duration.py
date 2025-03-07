# crud/duration.py
import json
import datetime
from datetime import timedelta
from fastapi import Query
async def calculate_duration(user_id=None, start_date=None):
    """
    Kullanıcıların içeride kaldığı süreleri hesaplar.
    
    Args:
        user_id (str, optional): Belirli bir kullanıcının süresini hesaplamak için ID.
        start_date (str, optional): Başlangıç tarihi (format: "DD.MM.YYYY").
        
    Returns:
        list: Her kullanıcı için içeride kalma süreleri.
    """
    try:
        # Log dosyasını oku
        try:
            with open("./log.json", "r", encoding="utf-8") as file:
                logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Tarih filtresi varsa uygula
        if start_date:
            try:
                start_datetime = datetime.datetime.strptime(start_date, "%d.%m.%Y")
                # Timestamp'i datetime'a çevirip filtreleme yap
                logs = [log for log in logs if datetime.datetime.fromisoformat(log.get("timestamp", "").split("+")[0]) >= start_datetime]
            except ValueError:
                # Tarih formatı hatalıysa filtreleme yapma
                print(f">> Hatalı tarih formatı: {start_date}")
        
        # Kullanıcı ID'si varsa filtrele
        if user_id:
            logs = [log for log in logs if log.get("user_id") == str(user_id)]
        
        # Önce logları kullanıcı ID'sine göre grupla
        user_logs = {}
        for log in logs:
            user_id = log.get("user_id")
            if not user_id:
                continue
                
            if user_id not in user_logs:
                user_logs[user_id] = []
            user_logs[user_id].append(log)
        
        # Her kullanıcı için giriş-çıkış çiftlerini bul ve süreleri hesapla
        duration_results = []
        
        for uid, user_logs_list in user_logs.items():
            # Logları zamana göre sırala (eskiden yeniye)
            user_logs_list.sort(key=lambda x: x.get("timestamp", ""))
            
            # Kullanıcının adını al
            user_name = user_logs_list[0].get("user_name") if user_logs_list else "Bilinmeyen Kullanıcı"
            
            # Giriş-çıkış eşleştirmelerini yap
            entry_exit_pairs = []
            last_entry = None
            
            for log in user_logs_list:
                action = log.get("action")
                
                if action == "entry":
                    last_entry = log
                elif action == "exit" and last_entry:
                    # Giriş ve çıkış zamanlarını al
                    entry_time = datetime.datetime.fromisoformat(last_entry.get("timestamp").split("+")[0])
                    exit_time = datetime.datetime.fromisoformat(log.get("timestamp").split("+")[0])
                    
                    # Süreyi hesapla
                    duration = exit_time - entry_time
                    
                    # Çifti kaydet
                    entry_exit_pairs.append({
                        "entry_time": last_entry.get("time"),
                        "exit_time": log.get("time"),
                        "duration_seconds": duration.total_seconds(),
                        "duration_formatted": format_duration(duration)
                    })
                    
                    last_entry = None
            
            # Hala içeride olan kullanıcı için (çıkış kaydı yoksa)
            if last_entry:
                now = datetime.datetime.now()
                entry_time = datetime.datetime.fromisoformat(last_entry.get("timestamp").split("+")[0])
                duration = now - entry_time
                
                entry_exit_pairs.append({
                    "entry_time": last_entry.get("time"),
                    "exit_time": "Hala içeride",
                    "duration_seconds": duration.total_seconds(),
                    "duration_formatted": format_duration(duration)
                })
            
            # Toplam süreyi hesapla
            total_seconds = sum(pair["duration_seconds"] for pair in entry_exit_pairs)
            total_duration = format_duration(timedelta(seconds=total_seconds))
            
            # Sonuçları kaydet
            duration_results.append({
                "user_id": uid,
                "user_name": user_name,
                "entries_count": len(entry_exit_pairs),
                "total_duration": total_duration,
                "total_seconds": total_seconds,
                "entries": entry_exit_pairs
            })
        
        # Sonuçları toplam süreye göre sırala (en uzun süre en üstte)
        duration_results.sort(key=lambda x: x.get("total_seconds", 0), reverse=True)
        
        return duration_results
        
    except Exception as e:
        print(f">> Süre hesaplama hatası: {str(e)}")
        return []

def format_duration(duration):
    """
    Timedelta süresini saat:dakika formatına çevirir.
    
    Args:
        duration (timedelta): Süre
        
    Returns:
        str: "HH:MM" formatında süre
    """
    total_seconds = duration.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    
    return f"{hours}:{minutes:02d}"