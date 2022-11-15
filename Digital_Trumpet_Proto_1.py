import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # BOARD or BCM
GPIO.setwarnings(False)

# These pin values are the GPIO numbers, not the pin number
valve1 = 16 # pin 36
valve2 = 20 # pin 38
valve3 = 21 # pin 40
mouthpiece = 12 # pin 32

buzzerpin = 19 # pin 35

# GPIO setup
GPIO.setup(valve1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzerpin, GPIO.OUT)

def Buzz(buzzPin,freq,duration_ms):
    duration_s = duration_ms / 1000
    buzzer = GPIO.PWM(buzzPin,freq)
    buzzer.start(10)
    time.sleep(duration_s)
    buzzer.stop


try:
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            if GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW:
                Buzz(19,262,10) # C (262 Hz)
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:
                Buzz(19,278,10) # C# (278 Hz)
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH:
                Buzz(19,294,10) # D (294 Hz)
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:
                Buzz(19,311,10) # D# (311 Hz)
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW:
                Buzz(19,330,10) # E (330 Hz)
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH:
                Buzz(19,330,10) # E (Alternate fingering)
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW:
                Buzz(19,349,10) # F (349 Hz)
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW:
                Buzz(19,370,10) # F# (370 Hz)     
finally:
    GPIO.cleanup()
