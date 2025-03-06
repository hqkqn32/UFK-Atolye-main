import RPi.GPIO as GPIO
import time

def gpio(pin,action):
    if action=="opendoor":
        GPIO.output(pin, GPIO.HIGH)  # Kapıyı aç
        time.sleep(2)  # 2 saniye bekle
        GPIO.output(pin, GPIO.LOW)  # Kapıyı kapat
    elif action=="light":
        current_state = GPIO.input(pin)
        GPIO.output(pin, not current_state)
        print(f"PIN {pin} durumu değiştirildi: {'HIGH' if not current_state else 'LOW'}")
    elif action=="light_on":
        current_state = GPIO.input(pin)
        GPIO.output(pin, GPIO.HIGH)
        print(f"PIN {pin} durumu değiştirildi: {'HIGH' if not current_state else 'LOW'}")
    elif action=="light_off":
        GPIO.output(pin, GPIO.LOW)