from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"


def sample_sustain(sound):
	frequency = find_frequency(file_name)
	wavelength = 1 / frequency
	duration = wavelength * 10 # * (# of wavelengths)
	dur_ms = duration * 1000 # duration is in seconds, change it to milliseconds
	extract = sound[300:300+dur_ms] # difference of about 10x wavelength
	extract.export(f"Samples/{instrument}/{mute}/Sound/Sustain/{file_name}_Sustain.wav", format="wav")
	return None
	
def sample_attack(sound_file):
	extract = sound[0:200]
	extract.export(f"Samples/{instrument}/{mute}/Sound/Attack/{file_name}_Attack.wav", format="wav")
	return None

def sample_release(sound_file):
	extract = sound[-201:-1]
	extract.export(f"Samples/{instrument}/{mute}/Sound/Release/{file_name}_Release.wav", format="wav")
	return None

def detect_silence(sound_file,silence_threshold=-50.0, chunk_size=10): # https://stackoverflow.com/questions/29547218/remove-silence-at-the-beginning-and-at-the-end-of-wave-files-with-pydub
	trim_ms = 0
	assert chunk_size > 0
	while sound_file[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
		trim_ms += chunk_size
	return trim_ms
	
def find_frequency(note):
	if note == 'C6':
		return 1046.5
	elif note == 'C#6':
		return 1108.73
	elif note == 'D6':
		return 1174.66
	elif note == "D#6":
		return 1244.51

# -----------------------------------------------------------------------------------------------


file_name = input("File name: ")
sound = AudioSegment.from_wav(f"Samples/{instrument}/{mute}/Sound/Complete/{file_name}.wav")

start_trim = detect_silence(sound)
end_trim = detect_silence(sound.reverse())

trimmed_sound = sound[start_trim:len(sound)-end_trim]

sample_sustain(trimmed_sound)
sample_attack(trimmed_sound)
sample_release(trimmed_sound)
# Sustain, then
# Attack, then
# End
