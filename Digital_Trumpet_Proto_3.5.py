import RPi.GPIO as GPIO
import time
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

sound_dir = "Trumpet_Samples/Sound"
attack_dir = "Trumpet_Samples/Sound/Attack"
sustain_dir = "Trumpet_Samples/Sound/Sustain"
release_dir = "Trumpet_Samples/Sound/Release"

# Load the sample pitches
# pygames didnt like 32bit floats (they need to be 16bit pcms, not 32bit floats)
# haven't tested with others like pydub
# pydub doesn't seem to like them either
# maybe pyaudio is fine with them???
    
sound_release = [
#     pydub.AudioSegment.from_wav(f"{sound_dir}C4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}C_sharp4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}D4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}D_sharp4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}Release/E4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}F4_release.wav"),
#     pydub.AudioSegment.from_wav(f"{sound_dir}F_sharp4_release.wav")
]

# Sound dictionary to tie notes and their sound

sound_sustain_dict = {
            'c4': f"{sustain_dir}/C4_Sustain.wav",
            'c#4': f"{sustain_dir}/C_sharp4_Sustain.wav",
            'd4': f"{sustain_dir}/D4_Sustain.wav",
            'd#4': f"{sustain_dir}/D_sharp4_Sustain.wav",
            'e4': f"{sustain_dir}/E4_Sustain.wav",
            'e_alt4': f"{sustain_dir}/E4_Sustain.wav",
            'f4': f"{sustain_dir}/F4_Sustain.wav",
            'f#4': f"{sustain_dir}/F_sharp4_Sustain.wav"
              }
sound_dict = {
            'c4': f"{sound_dir}/C4.wav",
            'c#4': f"{sound_dir}/C_sharp4.wav",
            'd4': f"{sound_dir}/D4.wav",
            'd#4': f"{sound_dir}/D_sharp4.wav",
            'e4': f"{sound_dir}/E4.wav",
            'e_alt4': f"{sound_dir}/E4.wav",
            'f4': f"{sound_dir}/F4.wav",
            'f#4': f"{sound_dir}/F_sharp4.wav"
            }

sound_release_dict = {
            'c4': f"{sound_dir}/C4.wav",
            'c#4': f"{sound_dir}/C_sharp4.wav",
            'd4': f"{sound_dir}/D4.wav",
            'd#4': f"{sound_dir}/D_sharp4.wav",
            'e4': f"{sound_dir}/E4.wav",
            'e_alt4': f"{sound_dir}/E4.wav",
            'f4': f"{sound_dir}/F4.wav",
            'f#4': f"{sound_dir}/F_sharp4.wav"
            }

# Valve combination to note, subject to change

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): 'c4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): 'c#4',
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): 'd4',
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): 'd#4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): 'e4',
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): 'e_alt4',
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): 'f4',
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): 'f#4'}
global is_playing
global my_thread
array_id = None
loop_var = 0
volume = 0

def play(wav_file):
    global is_playing
    is_playing = True
    chunk = 1024
    while is_playing == True:
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
        
        data = wf.readframes(chunk)
        
#         while data == '' and is_playing == True:
#             stream.write(chr(0)*chunk*channels*2)

        while data != '' and is_playing == True:
            stream.write(data)
            data = wf.readframes(chunk)

        # after the sound is done playing
        stream.stop_stream()
        stream.close()
    


try:
# https://stackoverflow.com/questions/47513950/how-to-loop-play-an-audio-with-pyaudio [currently working on implementing] [uses threading]
    while True:
        if GPIO.input(mouthpiece) == GPIO.HIGH:
            valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
            note_name = valve_dict[valves]
            if loop_var == 0:
                is_playing = True
                my_thread = threading.Thread(target=play,args = [sound_dict[note_name]])
                my_thread.start()
                time.sleep(.05)
            elif loop_var > 0:
                my_thread = threading.Thread(target=play,args = [sound_dict[note_name]])
                my_thread.start()
                time.sleep(1)
            else:
                continue
            print(note_name)
            print(loop_var)
            loop_var += 1
        else:
            loop_var = 0
            if array_id != None:
                my_thread = threading.Thread(target=play, args = [sound_array[array_id]])    
                print("Note ending")
                array_id = None
            else:
                continue
            is_playing = False
            print("Note stopped")
finally:
    is_playing = False
    print("Error")
    GPIO.cleanup()