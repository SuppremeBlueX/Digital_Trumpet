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

upper_octave = 2 # (GPIO 2)
lower_octave = 3 # (GPIO 3)

reg_0 = 21
reg_1 = 20
reg_2 = 16
reg_3 = 12
reg_4 = None
reg_5 = None
reg_6 = None
reg_7 = None
reg_8 = None
reg_9 = None
reg_10 = None
reg_11 = None

# GPIO setup
GPIO.setup(valve1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(upper_octave, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(lower_octave, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(mouthpiece, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(reg_0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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

_ = GPIO.HIGH
T = GPIO.LOW
slurred = True

# Valve combination to note, subject to change / will have a analog (potentiometer/pressure sensor) 
# variable in the future

simple_valve_dict = {
            (T,T,T): 'c4',
            (_,_,_): 'c#4',
            (_,T,_): 'd4',
            (T,_,_): 'd#4',
            (_,_,T): 'e4',
            (T,T,_): 'e4_alt',
            (_,T,T): 'f4',
            (T,_,T): 'f#4'
            }

advanced_valve_dict = {
            ('reg_0',_,_,_): 'f#3',
            ('reg_0',_,T,_): 'g3',
            ('reg_0',T,_,_): 'g#3',
            ('reg_0',_,_,T): 'a3',
            ('reg_0',T,T,_): 'a3_alt',
            ('reg_0',_,T,T): 'a#3',
            ('reg_0',T,_,T): 'b3',
            ('reg_1',T,T,T): 'c4',
            ('reg_1',_,_,_): 'c#4',
            ('reg_1',_,T,_): 'd4',
            ('reg_1',T,_,_): 'd#4',
            ('reg_1',_,_,T): 'e4',
            ('reg_1',T,T,_): 'e4_alt',
            ('reg_1',_,T,T): 'f4',
            ('reg_1',T,_,T): 'f#4',
            ('reg_2',_,_,_): 'f#4_alt',
            ('reg_2',T,T,T): 'g4',
            ('reg_2',_,T,_): 'g4_alt',
            ('reg_2',T,_,_): 'g#4',
            ('reg_2',_,_,T): 'a4',
            ('reg_2',T,T,_): 'a4_alt',
            ('reg_2',_,T,T): 'a#4',
            ('reg_2',T,_,T): 'b4',
            ('reg_3',T,T,T): 'c5',
            ('reg_3',_,_,T): 'c#5',
            ('reg_3',_,T,T): 'd5',
            ('reg_3',T,_,T): 'd#5',
            ('reg_4',T,T,T): 'e5',
            ('reg_4',_,T,T): 'f5',
            ('reg_4',T,_,T): 'f#5',
            ('reg_5',T,T,T): 'g5',
            ('reg_5',T,_,_): 'g#5',
            ('reg_5',_,_,T): 'a5',
            ('reg_5',_,T,T): 'a#5',
            ('reg_5',T,_,T): 'b5',
            ('reg_6',T,T,T): 'c6'
            }


# Handle interrupt event
interrupt_event = threading.Event()
def handle_interrupt(signal, frame):
    interrupt_event.set()
signal.signal(signal.SIGINT, handle_interrupt)

# in the future, there will be code to specifically pick up volume, but for now, return 1   
def get_volume_level():
    return 4

def change_octave(direction, note): # this function converts a note to another based on octave direction
      note_num = note.split('_')[0][-1]
      if direction == "Upper":
            updated_note_num = str(int(note_num) + 1)
      elif direction == "Lower":
            updated_note_num = str(int(note_num) - 1)
      else:
            raise Exception
      updated_note = (note.replace(note_num,updated_note_num)).split("_"[0])
      
      return updated_note

def check_register(): # I'm essentially making this function as a switch-case
      if GPIO.input(reg_0) == GPIO.HIGH:
            return 'reg_0'
      elif GPIO.input(reg_1) == GPIO.HIGH:
            return 'reg_1'
      elif GPIO.input(reg_2) == GPIO.HIGH:
            return 'reg_2'
      elif GPIO.input(reg_3) == GPIO.HIGH:
            return 'reg_3'
      elif GPIO.input(reg_4) == GPIO.HIGH:
            return 'reg_4'
      elif GPIO.input(reg_5) == GPIO.HIGH:
            return 'reg_5'
      elif GPIO.input(reg_6) == GPIO.HIGH:
            return 'reg_6'
      elif GPIO.input(reg_7) == GPIO.HIGH:
            return 'reg_7'
      elif GPIO.input(reg_8) == GPIO.HIGH:
            return 'reg_8'
      elif GPIO.input(reg_9) == GPIO.HIGH:
            return 'reg_9'
      elif GPIO.input(reg_10) == GPIO.HIGH:
            return 'reg_10'
      elif GPIO.input(reg_11) == GPIO.HIGH:
            return 'reg_11'
      else:
            return None

def transpose(original_key, new_key, note): # might play with this later
      key_list = ['C','C#','Db','D','D#','Eb','E','F','F#','Gb','G','G#','Ab','A','A#','Bb','B']
      return None

note_name = None
old_note = None
while not interrupt_event.is_set():
    # set some variables to keep track of the note currently played and the last note played
    if note_name != None or old_note != None:
        note_name = None
        old_note = None
    while GPIO.input(mouthpiece) == GPIO.HIGH:
        # what valve combination do I have?
        valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
        vw_reg = (check_register(), GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
        register = vw_reg[0]
        # translate the valve combination into the name of the note
        if register == None:
              note_name = simple_valve_dict[valves]
        else:
              note_name = advanced_valve_dict[vw_reg]
      
        # on the first iteration of the note, play the "attack"
        if old_note == None or slurred == False:
            old_note = note_name
            data, samplerate = sf.read(sound_attack_dict[note_name])
            data_vol = get_volume_level() * data
            sd.play(data_vol, samplerate,blocking=True)
        # on every other iteration of the note, play the "sustain"
        else:
            # grab data
            data, samplerate = sf.read(sound_sustain_dict[note_name])
            # integrate volume change to the data
            data_vol = get_volume_level() * data 
            # this actually plays the note
            if note_name != old_note:
                old_note = note_name
                sd.play(data_vol, samplerate,loop=True)

    # note release once mouthpiece is not active,   
    if note_name != None: # if there is a note currently playing
          
        # play the note release file
        data, samplerate = sf.read(sound_release_dict[note_name])
        data_vol = get_volume_level() * data
        sd.play(data_vol, samplerate,blocking=True)
        
        # reset variables
        note_name = None
        old_note = None
        loop_var = 0
    
#final cleanup
sd.stop()
GPIO.cleanup()


''' Notes:
1-22-24: Finally realized why my project isn't working, you don't ground buttons...

looking into adding more registers. Looking at 8-way rotary switch right now.

(pressure sensor would be ideal (except I don't know how to program for them yet), but I need a way to shift between registers)

created Proto_4.5

1-24-24: Looking into an 8-way or 12-way rotary switch. Now that I think about it, how well would this work on a breadboard? Might still try it anyways though.

Added reg_# variables so that program would work

Added slur variable to remove attacks from notes

having a problem with the first note not being played (the sustain, the attack is fine, and afterwards, I can go back to the note and it plays fine) Programming error? I don't see where the issue could be

Got it... I needed an AND instead of an OR...

1-31-24: I guess I didn't get it? I don't know why this isn't working properly anymore... There might be something wrong with how I'm implementing the variable.

2-5-24: The problem is still not fully solved, but that problem is isolated there. It won't affect the rest of my program. I need to implement a switch-case to check which input is on

Too bad Python doesn't have switch-cases... oh well... functions will work

'''
