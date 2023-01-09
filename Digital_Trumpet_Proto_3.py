import RPi.GPIO as GPIO
import time
import pydub
# added dependencies, pydub
from pydub.playback import play, _play_with_simpleaudio

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

sound_dir = "Trumpet_Samples/Sound/"

# Load the sample pitches (they need to be 16bit pcms, not 32bit floats)

sound_array = [
    pydub.AudioSegment.from_file(f"{sound_dir}C4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}C_sharp4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}D4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}D_sharp4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}E4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}F4.wav"),
    pydub.AudioSegment.from_file(f"{sound_dir}F_sharp4.wav")
]

sound_attack = []

sound_sustain = []
    
sound_release = []

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): ('c4',0),
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): ('c#4',1),
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): ('d4',2),
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): ('d#4',3),
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): ('e4',4),
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): ('e_alt4',4),
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): ('f4',5),
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): ('f#4',6)}
array_id = None

try:
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
            note_name, array_id = valve_dict[valves]
            print(note_name)
            play(sound_array[array_id])
            print("Note done playing")
            sound_playing = array_id
        else:
            continue
finally:
    GPIO.cleanup()