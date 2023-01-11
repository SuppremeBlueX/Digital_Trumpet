import pyaudio
import wave

note = "Trumpet_Samples/Sound/E4.wav"

chunk = 1024

wf = wave.open(note,'rb')

p = pyaudio.Pyaudio()

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

data = wf.readframes(chunk)

while data != '':
    stream.write(data)
    data = wf.readframes(chunk)
    
stream.close()
p.terminate()