# import GPIO from Raspberry Pi
import RPi.GPIO as GPIO

import soundfile as sf
# added dependancy: soundfile; need to pip3 install it
import sounddevice as sd
# added dependancy: sounddevice; need to pip3 install it
# also need PyAudio or Portaudio, possibly even both
import signal
# added dependancy: signal
import threading

# Raspberry Pi Setup
GPIO.setmode(GPIO.BCM) # The options are BOARD or BCM. BCM works
GPIO.setwarnings(False)

# These pin values are the GPIO numbers, not the pin number
valve1 = 7 # (GPIO 7)
valve2 = 8 # (GPIO 8)
valve3 = 25 # (GPIO 25)
mouthpiece = 1 # (GPIO 1)

# GPIO setup
GPIO.setup(valve1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define Instrument
Instrument = "Bb_Trumpet"
# Define Mute: "Unmuted" is the default
Mute = "Unmuted"
# Directory: Samples/Instrument/Mute/Sound/
sound_dir = f"Samples/{Instrument}/{Mute}/Sound"
attack_dir = f"{sound_dir}/Attack"
sustain_dir = f"{sound_dir}/Sustain"
release_dir = f"{sound_dir}/Release"

# sound dictionaries
# note names here are in the transposition of a Bb trumpet, not concert pitch
# Any samples of different instruments can either be in its key or its transposition, but specify it!

# test dictionary, will not be used in final code
sound_dict = {
            'c4': f"{sound_dir}/C4.wav", # Concert A# (also Bb)
            'c#4': f"{sound_dir}/C_sharp4.wav", # Concert B
            'd4': f"{sound_dir}/D4.wav", # Concert C
            'd#4': f"{sound_dir}/D_sharp4.wav", # Concert C# (also Db)
            'e4': f"{sound_dir}/E4.wav", # Concert D
            'e4_alt': f"{sound_dir}/E4.wav", # Concert D (Alternate fingering)
            'f4': f"{sound_dir}/F4.wav", # Concert D# (also Eb)
            'f#4': f"{sound_dir}/F_sharp4.wav" # Concert E
            }

#dictionaries to use in the final code
sound_attack_dict = {
            'c4': f"{attack_dir}/C4_Attack.wav",
            'c#4': f"{attack_dir}/C_sharp4_Attack.wav",
            'd4': f"{attack_dir}/D4_Attack.wav",
            'd#4': f"{attack_dir}/D_sharp4_Attack.wav",
            'e4': f"{attack_dir}/E4_Attack.wav",
            'e4_alt': f"{attack_dir}/E4_Attack.wav",
            'f4': f"{attack_dir}/F4_Attack.wav",
            'f#4': f"{attack_dir}/F_sharp4_Attack.wav"
              }

sound_sustain_dict = {
            'c4': f"{sustain_dir}/C4_Sustain.wav",
            'c#4': f"{sustain_dir}/C_sharp4_Sustain.wav",
            'd4': f"{sustain_dir}/D4_Sustain.wav",
            'd#4': f"{sustain_dir}/D_sharp4_Sustain.wav",
            'e4': f"{sustain_dir}/E4_Sustain.wav",
            'e4_alt': f"{sustain_dir}/E4_Sustain.wav",
            'f4': f"{sustain_dir}/F4_Sustain.wav",
            'f#4': f"{sustain_dir}/F_sharp4_Sustain.wav"
              }

sound_release_dict = {
            'c4': f"{release_dir}/C4_Release.wav",
            'c#4': f"{release_dir}/C_sharp4_Release.wav",
            'd4': f"{release_dir}/D4_Release.wav",
            'd#4': f"{release_dir}/D_sharp4_Release.wav",
            'e4': f"{release_dir}/E4_Release.wav",
            'e4_alt': f"{release_dir}/E4_Release.wav",
            'f4': f"{release_dir}/F4_Release.wav",
            'f#4': f"{release_dir}/F_sharp4_Release.wav"
            }

# Valve combination to note, subject to change / will have a analog (potentiometer/pressure sensor) 
# variable in the future

simple_valve_dict = {(GPIO.LOW,GPIO.LOW,GPIO.LOW): 'c4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH): 'c#4',
              (GPIO.HIGH,GPIO.LOW,GPIO.HIGH): 'd4',
              (GPIO.LOW,GPIO.HIGH,GPIO.HIGH): 'd#4',
              (GPIO.HIGH,GPIO.HIGH,GPIO.LOW): 'e4',
              (GPIO.LOW,GPIO.LOW,GPIO.HIGH): 'e4_alt',
              (GPIO.HIGH,GPIO.LOW,GPIO.LOW): 'f4',
              (GPIO.LOW,GPIO.HIGH,GPIO.LOW): 'f#4'}

# Handle interrupt event
interrupt_event = threading.Event()
def handle_interrupt(signal, frame):
    interrupt_event.set()
signal.signal(signal.SIGINT, handle_interrupt)

# in the future, there will be code to specifically pick up volume, but for now, return 1   
def get_volume_level():
    return 4

while not interrupt_event.is_set():
    # set some variables to keep track of the note currently played and the last note played
    note_name = None
    old_note = None
    loop_var = 0
    while GPIO.input(mouthpiece) == GPIO.HIGH:
        # what valve combination do I have?
        valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
        # translate the valve combination into the name of the note
        note_name = simple_valve_dict[valves]
        # on the first iteration of the note, play the "attack"
        if loop_var == 0:
            data, samplerate = sf.read(sound_attack_dict[note_name])
            data_vol = get_volume_level() * data 
            loop_var += 1
            print("Attack Read")
            sd.play(data_vol, samplerate,blocking=True)
        # on every other iteration of the note, play the "sustain"
        else:
            # grab data
            data, samplerate = sf.read(sound_sustain_dict[note_name])
            # integrate volume change to the data
            data_vol = get_volume_level() * data 
            print("Sustain Read") # If this print statement is not here, the note underruns and does not sound good. We could also implement a sleep function. Not sure why this is happening
        # this actually plays the note
            if note_name != old_note:
                old_note = note_name
                sd.play(data_vol, samplerate,loop=True)

    # note release once mouthpiece is not active,   
    if note_name != None: # if there is a note currently playing
        # play the note release file
        data, samplerate = sf.read(sound_release_dict[note_name])
        data_vol = get_volume_level() * data
        print(f"{note_name} ending")
        sd.play(data_vol, samplerate,blocking=True)
        # reset variables
        note_name = None
        old_note = None
        loop_var = 0
    
#final cleanup
sd.stop()
GPIO.cleanup()
