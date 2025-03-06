import os
from dotenv import load_dotenv


# .env dosyasını yükle
load_dotenv()

# .env'den kullanıcı bilgilerini al
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "030378")

def verify_user(username, password):
   
    if username != ADMIN_USERNAME:
        return False
    
    if password != ADMIN_PASSWORD:
        return False
    
    return True
