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

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): ('c4',0)}

try:
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
            note_name, array_id = valve_dict[valves]
            sound_array[array_id].stop() 
            print(note_name)
            sound_array[array_id].play()
            
        else:
            sound_array[array_id].stop()
finally:
    GPIO.cleanup()
