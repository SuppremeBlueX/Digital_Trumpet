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

data, samplerate = sf.read("Trumpet_Samples/Sound/C4.wav")

volume = 1

interrupt_event = threading.Event()

def handle_interrupt(signal, frame):
    interrupt_event.set()
    
def get_volume_level():
    return 1

signal.signal(signal.SIGINT, handle_interrupt)

while not interrupt_event.is_set():
    
    volume = get_volume_level()
    
    data_vol = volume * data
    
    sd.play(data_vol, samplerate)
    
    sd.wait()
    
#final cleanup
sd.stop()
sd.close()