import json
def is_user(user_rfid):
    try:
        with open("user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
            
        user = next((u for u in users if u.get("rfid_id") == user_rfid), None)
        
        if user is None:
            return False
            
        return True
    except Exception as e:
        print(f"Hata: {str(e)}")
        return False