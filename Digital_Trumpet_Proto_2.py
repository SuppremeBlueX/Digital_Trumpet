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

# GPIO setup
GPIO.setup(valve1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize Pygame Mixer
mixer.init()

sample_dir = "Trumpet_Samples/Sound/"

# Load the sample pitches (they need to be 16bit pcms, not 32bit floats)

sound_array = [
    mixer.Sound(f"{sample_dir}C4.wav"),
    mixer.Sound(f"{sample_dir}C_sharp4.wav"),
    mixer.Sound(f"{sample_dir}D4.wav"),
    mixer.Sound(f"{sample_dir}D_sharp4.wav"),
    mixer.Sound(f"{sample_dir}E4.wav"),
    mixer.Sound(f"{sample_dir}F4.wav"),
    mixer.Sound(f"{sample_dir}F_sharp4.wav")
]

array_id = None

try:
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            if GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW: # C
                if array_id != 0:
                    if array_id != None: # Null check
                        sound_array[array_id].stop() 
                    print("c")
                    array_id = 0
                    sound_array[array_id].play()
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:  # C#
                if array_id != 1:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("c#")
                    array_id = 1
                    sound_array[array_id].play()
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH:  # D
                if array_id != 2:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("D")
                    array_id = 2
                    sound_array[array_id].play()
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.HIGH:  # D#
                if array_id != 3:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("D#")
                    array_id = 3
                    sound_array[array_id].play()
            elif (GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW) or (GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.HIGH):  # E (including alternate fingering)
                if array_id != 4:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("E")
                    array_id = 4
                    sound_array[array_id].play()
            elif GPIO.input(valve1) == GPIO.HIGH and GPIO.input(valve2) == GPIO.LOW and GPIO.input(valve3) == GPIO.LOW:  # F
                if array_id != 5:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("F")
                    array_id = 5
                    sound_array[array_id].play()
            elif GPIO.input(valve1) == GPIO.LOW and GPIO.input(valve2) == GPIO.HIGH and GPIO.input(valve3) == GPIO.LOW:  # F
                if array_id != 6:
                    if array_id != None:
                        sound_array[array_id].stop()
                    print("F#")
                    array_id = 6
                    sound_array[array_id].play()
        else:
            if array_id != None:
                sound_array[array_id].stop()
            array_id = None
finally:
    GPIO.cleanup()