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

sound_array = [
    mixer.Sound(f"{sample_dir}C4.wav"),
    mixer.Sound(f"{sample_dir}C_sharp4.wav"),
    mixer.Sound(f"{sample_dir}D.wav"),
    mixer.Sound(f"{sample_dir}D_sharp.wav"),
    mixer.Sound(f"{sample_dir}E.wav"),
    mixer.Sound(f"{sample_dir}F.wav"),
    mixer.Sound(f"{sample_dir}F_sharp.wav")
]
array_int = NULL

try:
    while True:
        
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            if GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW: # C
                if array_int != 0:
                    sound_array[array_int].stop()
                print("c")
                array_int = 0
                sound_array[array_int].play() 
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:  # C#
                if array_int != 1:
                    sound_array[array_int].stop()
                    print("c#")
                    array_int = 1
                    sound_array[array_int].play()
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH:  # D
                if array_int != 2:
                    sound_array[array_int].stop()
                    print("D")
                    array_int = 2
                    sound_array[array_int].play()
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:  # D#
                if array_int != 3:
                    sound_array[array_int].stop()
                    print("D#")
                    array_int = 3
                    sound_array[array_int].play()
            elif (GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW) or (GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH):  # E (including alternate fingering)
                if array_int != 4:
                    sound_array[array_int].stop()
                    print("E")
                    array_int = 4
                    sound_array[array_int].play()
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW:  # F
                if array_int != 5:
                    sound_array[array_int].stop()
                    print("F")
                    array_int = 5
                    sound_array[array_int].play()
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW:  # F
                if array_int != 6:
                    sound_array[array_int].stop()
                    print("F#")
                    array_int = 6
                    sound_array[array_int].play()
finally:
    GPIO.cleanup()
