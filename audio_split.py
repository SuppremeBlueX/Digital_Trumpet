from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"


def sample_sustain(sound):
	max_amplitude = sound.max
	#soundleft, soundright = sound.split_to_mono()
	samples = sound.get_array_of_samples()
	peaked = False
	peak = 0
	percent = 0.9
	for start, sample in enumerate(samples):
		if sample >= (percent * max_amplitude):
			if peaked == False:      
				peak = peak + 1
				peaked = True
		else:
			peaked = False

	for end, sample in enumerate(reversed(samples)):
		if sample >= (percent * max_amplitude):
			break
	print(peak)
	extract = sound._spawn(samples[start:-end]) # negate end because we're counting from the end
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
# -----------------------------------------------------------------------------------------------


file_name = input("File name: ")
sound = AudioSegment.from_wav(f"Samples/{instrument}/{mute}/Sound/Complete/{file_name}.wav")

start_trim = detect_silence(sound)
end_trim = detect_silence(sound.reverse())

sound = sound[start_trim:len(sound)-end_trim]

print(f"Max = {sound.max}")
print(f"Normalized = {sound.normalize()}")

sample_sustain(sound)
sample_attack(sound)
sample_release(sound)
# Sustain, then
# Attack, then
# End
