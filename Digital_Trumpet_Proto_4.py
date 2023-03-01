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

# Define Instrument
Instrument = "Bb_Trumpet"
# Define Mute: "Unmuted" is the default
Mute = "Unmuted"
# directories for Trumpet Samples
sound_dir = f"Samples/{Instrument}/{Mute}/Sound"
attack_dir = f"{sound_dir}/Attack"
sustain_dir = f"{sound_dir}/Sustain"
release_dir = f"{sound_dir}/Release"

# sound dictionaries
# note names here are in the transposition of a Bb trumpet, not concert pitch
# Any samples of different instruments can either be in its key or its transposition, but specify it!
sound_dict = {
            'c4': f"{sound_dir}/C4.wav", # Concert Bb (also A#)
            'c#4': f"{sound_dir}/C_sharp4.wav", # Concert B
            'd4': f"{sound_dir}/D4.wav", # Concert C
            'd#4': f"{sound_dir}/D_sharp4.wav", # Concert C# (also Db)
            'e4': f"{sound_dir}/E4.wav", # Concert D
            'e_alt4': f"{sound_dir}/E4.wav", # Concert D (Alternate fingering)
            'f4': f"{sound_dir}/F4.wav", # Concert Eb (also D#)
            'f#4': f"{sound_dir}/F_sharp4.wav" # Concert E
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
            'c4': f"{release_dir}/C4_Release.wav",
            'c#4': f"{release_dir}/C_sharp4_Release.wav",
            'd4': f"{release_dir}/D4_Release.wav",
            'd#4': f"{release_dir}/D_sharp4_Release.wav",
            'e4': f"{release_dir}/E4_Release.wav",
            'e_alt4': f"{release_dir}/E4_Release.wav",
            'f4': f"{release_dir}/F4_Release.wav",
            'f#4': f"{release_dir}/F_sharp4_Release.wav"
            }

# Valve combination to note, subject to change / will have a analog (potentiometer/pressure sensor) 
# variable in the future

valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): 'c4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): 'c#4',
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): 'd4',
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): 'd#4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): 'e4',
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): 'e4_alt',
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): 'f4',
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): 'f#4'}

# set some global variables to keep track of the note currently played and the last note played
note_name = None
old_note = None

interrupt_event = threading.Event()

def handle_interrupt(signal, frame):
    interrupt_event.set()
    
def get_volume_level():
    # in the future, there will be code to specifically pick up volume, but for now, return 1
    return 1

signal.signal(signal.SIGINT, handle_interrupt)
 
# keep sounds in memory

note_sound_dict = {
    # Attacks
    ('c4','a'): sf.read(f"{sound_attack_dict['c4']}"),
    ('c#4','a'): sf.read(f"{sound_attack_dict['c#4']}"),
    ('d4','a'): sf.read(f"{sound_attack_dict['d4']}"),
    ('d#4','a'): sf.read(f"{sound_attack_dict['d#4']}"),
    ('e4','a'): sf.read(f"{sound_attack_dict['e4']}"),
    ('e4_alt','a'): sf.read(f"{sound_attack_dict['e4']}"),
    ('f4','a'): sf.read(f"{sound_attack_dict['f4']}"),
    ('f#4','a'): sf.read(f"{sound_attack_dict['f#4']}"),
    # Sustains
    ('c4','s'): sf.read(f"{sound_sustain_dict['c4']}"),
    ('c#4','s'): sf.read(f"{sound_sustain_dict['c#4']}"),
    ('d4','s'): sf.read(f"{sound_sustain_dict['d4']}"),
    ('d#4','s'): sf.read(f"{sound_sustain_dict['d#4']}"),
    ('e4','s'): sf.read(f"{sound_sustain_dict['e4']}"),
    ('e4_alt','s'): sf.read(f"{sound_sustain_dict['e4']}"),
    ('f4','s'): sf.read(f"{sound_sustain_dict['f4']}"),
    ('f#4','s'): sf.read(f"{sound_sustain_dict['f#4']}"),
    # Releases
    ('c4','r'): sf.read(f"{sound_release_dict['c4']}"),
    ('c#4','r'): sf.read(f"{sound_release_dict['c#4']}"),
    ('d4','r'): sf.read(f"{sound_release_dict['d4']}"),
    ('d#4','r'): sf.read(f"{sound_release_dict['d#4']}"),
    ('e4','r'): sf.read(f"{sound_release_dict['e4']}"),
    ('e4_alt','r'): sf.read(f"{sound_release_dict['e4']}"),
    ('f4','r'): sf.read(f"{sound_release_dict['f4']}"),
    ('f#4','r'): sf.read(f"{sound_release_dict['f#4']}"),
    # ... more to come
    }
 
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
            data, samplerate = note_sound_dict[note_name,'a'] # 'a' for attack
            loop_var += 1
            print("Attack Read")
            sd.play(data, samplerate,blocking=True)
        # on every other iteration of the note, play the "sustain"
        else:
            # set the volume
            volume = get_volume_level()
            # grab data
            data, samplerate = note_sound_dict[note_name,'s'] # 's' for sustain
            # integrate volume change to the data
            data_vol = volume * data 
            print("Sustain Read") # If this print statement is not here, the note underruns and does not sound good. We could also implement a sleep function
        # this actually plays the note
            if note_name != old_note:
                
                old_note = note_name
                sd.play(data, samplerate,loop=True)
        
        # wait until the note is complete
        #sd.wait()

    #note release once mouthpiece is not active,
    
    if note_name != None: # if there is a note currently playing
        # play the note release file
        data, samplerate = note_sound_dict[note_name,'r'] # 'r' for release
        volume = get_volume_level()
        data_vol = volume * data
        print(f"{note_name} ending")
        sd.play(data_vol, samplerate)
        sd.wait()
        # reset variables
        note_name = None
        old_note = None
        loop_var = 0
    
#final cleanup
sd.stop()