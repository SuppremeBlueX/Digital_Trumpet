# import GPIO from Raspberry Pi
import RPi.GPIO as GPIO

import soundfile as sf
# added dependancy: soundfile; need to pip3 install it
import sounddevice as sd
# added dependancy: sounddevice; need to pip3 install it
import signal
# added dependancy: signal
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

# directories for Trumpet Samples
sound_dir = "Trumpet_Samples/Sound"
attack_dir = "Trumpet_Samples/Sound/Attack"
sustain_dir = "Trumpet_Samples/Sound/Sustain"
release_dir = "Trumpet_Samples/Sound/Release"

# sound dictionaries
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

sound_attack_dict = {
            'c4': f"{attack_dir}/C4_Attack.wav",
            'c#4': f"{attack_dir}/C_sharp4_Attack.wav",
            'd4': f"{attack_dir}/D4_Attack.wav",
            'd#4': f"{attack_dir}/D_sharp4_Attack.wav",
            'e4': f"{attack_dir}/E4_Attack.wav",
            'e_alt4': f"{attack_dir}/E4_Attack.wav",
            'f4': f"{attack_dir}/F4_Attack.wav",
            'f#4': f"{attack_dir}/F_sharp4_Attack.wav"
              }

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

# Valve combination to note, subject to change / will have a potientiometer variable in the future

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): 'c4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): 'c#4',
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): 'd4',
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): 'd#4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): 'e4',
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): 'e_alt4',
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): 'f4',
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): 'f#4'}

note_name = None

data, samplerate = sf.read("Trumpet_Samples/Sound/C4.wav")

interrupt_event = threading.Event()

def handle_interrupt(signal, frame):
    interrupt_event.set()
    
def get_volume_level():
    # in the future, there will be code to specifically pick up volume, but for now, return 1
    return 1

signal.signal(signal.SIGINT, handle_interrupt)


loop_var = 0
while not interrupt_event.is_set():
    while GPIO.input(mouthpiece) == GPIO.HIGH:
        # what valve combination do I have?
        valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
        # translate the valve combination into the name of the note
        note_name = valve_dict[valves]
        
        # these notes are loaded, but not played yet
        # on the first iteration of the note, play the "attack"
        if loop_var == 0:
            data, samplerate = sf.read(f"{sound_attack_dict[note_name]}")
            loop_var += 1
        # on every other iteration of the note, play the "sustain"
        else:
            data, samplerate = sf.read(f"{sound_sustain_dict[note_name]}")
            
            
        # set the volume
        volume = get_volume_level()
        
        # integrate volume change to the data
        data_vol = volume * data
        
        # this actually plays the note
        sd.play(data_vol, samplerate)
        
        # wait until the note is complete
        sd.wait()

#note release
# if there is a note playing
if note_name != None:
    # play the note release file
    data, samplerate = sf.read(f"{sound_release_dict[note_name]}")
    volume = get_volume_level()
    data_vol = volume * data
    sd.play(data_vol, samplerate)
    sd.wait()
    
#final cleanup
sd.stop()