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
reg_4 = 24
reg_5 = 23
reg_6 = 18
reg_7 = 15
reg_8 = 14
reg_9 = 0
reg_10 = 0
reg_11 = 0

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
GPIO.setup(reg_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(reg_11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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

# This function will replace the lengthy dictionary I previously had
def sound_file_search(note, section):
      note = note.split('_')[0] # turns 'E4_Alt' into 'E4', etc.
      if section == "a":
            return f"{sound_dir}/Attack/{note}_Attack.wav"
      elif section == "s":
            return f"{sound_dir}/Sustain/{note}_Sustain.wav"
      elif section == "r":
            return f"{sound_dir}/Release/{note}_Release.wav"
      else:
            raise ValueError('You didn\'t correctly specify which part of the sound to play. Expected: \'a\',\'s\', or \'r\' ')


_ = GPIO.HIGH
T = GPIO.LOW

# Valve combination to note, subject to change / will have a analog (potentiometer/pressure sensor) 
# variable in the future

simple_valve_dict = {
            (T,T,T): 'C4',
            (_,_,_): 'C#4',
            (_,T,_): 'D4',
            (T,_,_): 'D#4',
            (_,_,T): 'E4',
            (T,T,_): 'E4_alt',
            (_,T,T): 'F4',
            (T,_,T): 'F#4'
            }

advanced_valve_dict = {
            ('reg_0',_,_,_): 'F#3',
            ('reg_0',_,T,_): 'G3',
            ('reg_0',T,_,_): 'G#3',
            ('reg_0',_,_,T): 'A3',
            ('reg_0',T,T,_): 'A3_alt',
            ('reg_0',_,T,T): 'A#3',
            ('reg_0',T,_,T): 'B3',
            ('reg_0',T,T,T): 'C4',
            ('reg_1',T,T,T): 'C4',
            ('reg_1',_,_,_): 'C#4',
            ('reg_1',_,T,_): 'D4',
            ('reg_1',T,_,_): 'D#4',
            ('reg_1',_,_,T): 'E4',
            ('reg_1',T,T,_): 'E4_alt',
            ('reg_1',_,T,T): 'F4',
            ('reg_1',T,_,T): 'F#4',
            ('reg_2',_,_,_): 'f#4_alt',
            ('reg_2',T,T,T): 'G4',
            ('reg_2',_,T,_): 'G4_alt',
            ('reg_2',T,_,_): 'G#4',
            ('reg_2',_,_,T): 'A4',
            ('reg_2',T,T,_): 'A4_alt',
            ('reg_2',_,T,T): 'A#4',
            ('reg_2',T,_,T): 'B4',
            ('reg_3',T,T,T): 'C5',
            ('reg_3',_,_,T): 'C#5',
            ('reg_3',_,T,T): 'D5',
            ('reg_3',T,_,T): 'D#5',
            ('reg_4',T,T,T): 'E5',
            ('reg_4',_,T,T): 'F5',
            ('reg_4',T,_,T): 'F#5',
            ('reg_5',T,T,T): 'G5',
            ('reg_5',T,_,_): 'G#5',
            ('reg_5',_,_,T): 'A5',
            ('reg_5',_,T,T): 'A#5',
            ('reg_5',T,_,T): 'B5',
            ('reg_6',T,T,T): 'C6',
            ('reg_6',_,_,T): 'C#6',
            ('reg_6',_,T,T): 'D6',
            ('reg_6',T,_,T): 'D#6',
            ('reg_7',T,T,T): 'E6'
            }


# Handle interrupt event
interrupt_event = threading.Event()
def handle_interrupt(signal, frame):
    interrupt_event.set()
signal.signal(signal.SIGINT, handle_interrupt)

# in the future, there will be code to specifically pick up volume, but for now, return 1   
def get_volume_level():
    return 1

def change_octave(direction, note): # this function converts a note to another based on octave direction
      note_num = note.split('_')[0][-1]
      if direction == "Upper":
            updated_note_num = str(int(note_num) + 1)
      elif direction == "Lower":
            updated_note_num = str(int(note_num) - 1)
      else:
            raise ValueError('The first parameter has to be either \'Upper\' or \'Lower\'')
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

loop_var = 0
note_name = None
old_note = None

unknown_count = 0
while not interrupt_event.is_set():
      try:
            # set some variables to keep track of the note currently played and the last note played
            if note_name != None or old_note != None:
              note_name = None
              old_note = None
            while GPIO.input(mouthpiece) == GPIO.HIGH:
              # what valve combination do I have?
              valves = (GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
              valves_reg = (check_register(), GPIO.input(valve1), GPIO.input(valve2),  GPIO.input(valve3))
              # translate the valve combination into the name of the note
              
              if valves_reg in advanced_valve_dict.keys():
                    note_name = advanced_valve_dict[valves_reg]
              else:
                    if valves_reg[0] == None:
                        note_name = simple_valve_dict[valves] # if no register, use the simple dict
              if note_name == None:
                    raise ValueError(f"Unknown Valve/Register combination")
            
              # on the first iteration of the note, play the "attack"
              if loop_var == 0:
                  data, samplerate = sf.read(sound_file_search(note_name,'a'))
                  unknown_count = 0
                  data_vol = get_volume_level() * data
                  sd.play(data_vol, samplerate,blocking=True)
                  print(f"{note_name} Attack")
              # on every other iteration of the note, play the "sustain"
              else:
                  # grab data
                  data, samplerate = sf.read(sound_file_search(note_name,'s'))
                  unknown_count = 0
                  # integrate volume change to the data
                  data_vol = get_volume_level() * data 
                  # this actually plays the note
                  if note_name != old_note:
                      old_note = note_name
                      sd.play(data_vol, samplerate,loop=True)
                      print(f"{note_name} Sustain")
              loop_var = loop_var + 1

            # note release once mouthpiece is not active,   
            if note_name != None: # if there is a note currently playing
                
              # play the note release file
              data, samplerate = sf.read(sound_file_search(note_name,'r'))
              unknown_count = 0
              data_vol = get_volume_level() * data
              sd.play(data_vol, samplerate,blocking=True)
              print(f"{note_name} Release")
              
              # reset variables
              note_name = None
              old_note = None
              loop_var = 0
      except sf.LibsndfileError:
            if (unknown_count == 0):
                  print(f"Unknown note {note_name} encountered.")
            elif (unknown_count == 100000):
                  print(f"Still pressing unknown note {note_name}")
            elif (unknown_count == 1000000):
                  print(f"Seriously???")
            elif (unknown_count == 10000000):
                  print(f"Please Stop")
            elif (unknown_count == 10000000):
                  print(f"How's your finger?")
            unknown_count += 1
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

2-12-24: Ok, I removed the problem. I was unneccesarily assigning a variable that made it so that my condition to play a sustained note will never play the first time.

Also, I removed the slurred variable. It's technically how you push the button that determines it. Holding the button slurs the notes, while pressing it tounges the note.

The audio_split code is ok, I got lucky with A#3, but the flaws are more obvious with others, where the wavelengths are not really lined up.

2-26-24: Breakthrough! I have finally (after discussing with Prof O to help me with the logic) figured out how to detect 'peaks'. With this function, I have a list of locations

of peaks which I can use to slice the sound files into (hopefully) perfect slices without any wavering in the noise.

'''
