import RPi.GPIO as GPIO
import time
import pydub
# added dependency: pydub
import pyaudio
# added dependency: pyaudio
import wave
import sys
import threading

# Raspberry Pi Setup
GPIO.setmode(GPIO.BCM) # BOARD or BCM
GPIO.setwarnings(False)

# These pin values are the GPIO numbers, not the pin number
valve1 = 16 # pin 36 (GPIO 16)
valve2 = 20 # pin 38 (GPIO 20)
valve3 = 21 # pin 40 (GPIO 21)
mouthpiece = 12 # pin 32 (GPIO 12)

# GPIO setup
GPIO.setup(valve1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

sound_dir = "Trumpet_Samples/Sound/"

# Load the sample pitches
# pygames didnt like 32bit floats (they need to be 16bit pcms, not 32bit floats)
# haven't tested with others like pydub
# pydub doesn't seem to like them either

sound_array = [
    pydub.AudioSegment.from_wav(f"{sound_dir}C4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}C_sharp4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}D4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}D_sharp4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}E4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}F4.wav"),
    pydub.AudioSegment.from_wav(f"{sound_dir}F_sharp4.wav")
]

sound_attack = []

sound_sustain = []
    
sound_release = [
#     pydub.AudioSegment.from_wav(f"{sound_dir}C4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}C_sharp4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}D4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}D_sharp4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}Release/E4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}F4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}F_sharp4_release.wav")
]

# Valve combination to note, and an ID (lowest note has to be ID: '0', then '1', '2', etc. Alternate Fingerings have the same ID as their normal counterparts)

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): ('c4',0),
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): ('c#4',1),
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): ('d4',2),
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): ('d#4',3),
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): ('e4',4),
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): ('e_alt4',4),
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): ('f4',5),
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): ('f#4',6)}
array_id = None
volume = 0
loop_var = 0

def play(wav_file,volume):
    global is_playing
    global my_thread
    chunk = 1024
    wf = wave.open(wav_file,'rb') #'rb' is read-only as opposed to 'wb': write only
    # wf is a Wave_read object with the following methods:
    # .close(): Closes the stream if it was opened by wave and makes the instance unusable. On object collection, this is called automatically
    # .getnchannels() Returns the number of audio channels
    # .getsampwidth() Returns the sample width in bytes
    # .getframerate() Returns the number of audio frames
    # There are more, but just look at https://docs.python.org/3/library/wave.html for the others

    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True) # Output determines whether or not the sound actually plays.
    
    data = wf.readframes(chunk*(volume/100)) # Test if this actually works (* (volume/100))

    while data != '' and is_playing:
        stream.write(data)
        data = wf.readframes(chunk*(volume/100)) # Test if this actually works (* (volume/100))

    # after the sound is done playing
    stream.stop_stream()
    stream.close()
    p.terminate()

try:
# https://stackoverflow.com/questions/47513950/how-to-loop-play-an-audio-with-pyaudio [currently working on implementing] [uses threading]
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
            note_name, array_id = valve_dict[valves]
            if loop_var == 0:
                is_playing = True
                my_thread = threading.Thread(target=play((sound_array[array_id])[:50])) # probably the most complex single line I've coded so far. The stack overflow link above helped a lot
                time.sleep(.05)
            elif loop_var > 0:
                my_thread = threading.Thread(target=play((sound_array[array_id])[2500:2600]))
                time.sleep(0.1)
            else:
                continue
            print(note_name)
            loop_var += 1
        else:
            loop_var = 0
            if array_id != None:
                my_thread = threading.Thread(target=play((sound_array[array_id])[3500:]))
                
                print("Note ending")
                array_id = None
            else:
                continue
            is_playing = False 
finally:
    GPIO.cleanup()