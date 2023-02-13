#Rewriting the code with a few changes, mainly adding the multiprocessing library
import RPi.GPIO as GPIO
import time
import pyaudio
# added dependency: pyaudio
import wave
import sys
from multiprocessing import Process, Lock

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

# directories for Trumpet Samples

sound_dir = "Trumpet_Samples/Sound"
attack_dir = "Trumpet_Samples/Sound/Attack"
sustain_dir = "Trumpet_Samples/Sound/Sustain"
release_dir = "Trumpet_Samples/Sound/Release"
    
# Sound dictionary to tie notes with their sound

# is pyaudio good with 32-bit floats, or do they need to be 16-bit PCMs?
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
is_playing = False
array_id = None
loop_var = 0
volume = 0

def play(wav_file, lock):
    lock.acquire()
    global is_playing
    is_playing = True
    chunk = 1024
    wf = wave.open(wav_file,'rb')
    p = pyaudio.PyAudio()
    stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True) # Output determines whether or not the sound actually plays.
    while is_playing == True:
        
        data = wf.readframes(chunk)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)

        # after the sound is done playing
        wf.rewind()
    # or when is_playing no longer applies
    stream.stop_stream()
    stream.close()
    lock.release()
    

if __name__ == '__main__':
    lock = Lock()
    try:
        while True:
            if GPIO.input(mouthpiece) == GPIO.HIGH:
                valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
                note_name = valve_dict[valves]
                if loop_var == 0:
                    Process(target=play,args=(sound_dict[note_name],lock)).start()
                    time.sleep(.2)
                elif loop_var > 0:
                    Process(target=play,args=(sound_sustain_dict[note_name],lock)).start()
                    time.sleep(.1)
                else:
                    continue
                print(note_name)
                print(loop_var)
                loop_var += 1
            else:
                loop_var = 0
                if array_id != None:
                    Process(target=play,args=(sound_dict[note_name],lock)).start()  
                    print("Note ending")
                    array_id = None
                else:
                    continue
                is_playing = False
                print("Note stopped")
    finally:
        is_playing = False
        GPIO.cleanup()
