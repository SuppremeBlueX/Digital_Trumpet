import RPi.GPIO as GPIO
import time
from pygame import mixer

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

# Initialize Pygame Mixer
mixer.init()

# 
sample_dir = "Trumpet_Samples/Sound/"

# Load the sample pitches (needed to be 16bit pcms)
# Use audacity to convert to 16bit PCMs

sound_c4 = mixer.Sound(f"{sample_dir}C4.wav")
sound_csharp4 = mixer.Sound(f"{sample_dir}C_sharp4.wav")
#sound_d4 = mixer.Sound(f"{sample_dir}D.wav")
#sound_dsharp4 = mixer.Sound(f"{sample_dir}D_sharp.wav")
#sound_e4 = mixer.Sound(f"{sample_dir}E.wav")
#sound_f4 = mixer.Sound(f"{sample_dir}F.wav")
#sound_fsharp4 = mixer.Sound(f"{sample_dir}F_sharp.wav")

try:
    while True:
        
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            if not mixer.get_busy():
                sound_c4.stop()
                sound_c4.play()
                time.sleep(3)
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW:
                print("c")
                #sound_c4.play() # C (262 Hz)
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:
                print("c#")
                #sound_csharp4.play() # C# (278 Hz)
        else:
            sound_c4.stop()
            sound_csharp4.stop()
finally:
    GPIO.cleanup()


