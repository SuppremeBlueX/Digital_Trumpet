from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"

def find_indices(sound):
	channels = 2
	s_start_index = None
	s_end_index = None
	a_start_index = None
	a_end_index = None
	r_start_index = None
	r_end_index = None
	max_amp = False 
	peak = 0
	peaks = []
	peaking = False
	marking_attack = False
	marking_sustain = False
	marking_release = False
	samples = sound.get_array_of_samples()
	for index, sample in enumerate(samples):
		if index % channels == 0: # turning this from stereo to mono, insignificant change in quality
			continue
		else:
			delta = samples[index] - samples[index-channels] # delta change
			if sample > 0 and delta < 0:
				if peaking == False:
					peak += 1
					# samples[index-channels] = (2**15)-1
					peaks.append(index-channels)
					peaking = True
#					if sample == sound.max:
#						max_amp = True
#					if sample < (0.5 * sound.max) and (max_amp == False) and (marking_attack == False):
#						marking_attack = True
#						print(f"Attack Start Index: {index}")
#						a_start_index = index
#					elif marking_attack == True:
#						a_end_index = index
#						print(f"Attack End Index: {index}")
#					if sample == (0.5 * sound.max):
#						print(f"Sustain Start Index: {index}")
#						marking_sustain = True
#						s_start_index = index
#					elif marking_sustain == True:
#						print(f"Sustain End Index: {index}")
#						s_end_index = index
#						marking_sustain = False
#					if sample == (0.5 * sound.max) and (max_amp == True):
#						marking_release = True
#						print(f"Release Start Index: {index}")
#						r_start_index = index
			elif sample < 0 and peaking == True:
				peaking = False
#		if marking_release == True:
#			print(f"Release End Index: {index}")
#			r_end_index = index
#			marking_release = False
			
	print(len(peaks))
	start_index = None
	end_index = None
	max_amplitude = sound.max
	samples = sound.get_array_of_samples()
	
	return s_start_index, s_end_index, a_start_index, a_end_index, r_start_index, r_end_index, samples

def sample(sound):
	s_start_index, s_end_index, a_start_index, a_end_index, r_start_index, r_end_index, samples = find_indices(sound)
	# export and extract sounds
	extract = sound._spawn(samples[s_start_index:s_end_index])
	extract.export(f"Samples/{instrument}/{mute}/Sound/Sustain/{file_name}_Sustain.wav", format="wav")
	extract = sound._spawn(samples[a_start_index:a_end_index])
	extract.export(f"Samples/{instrument}/{mute}/Sound/Attack/{file_name}_Attack.wav", format="wav")
	extract = sound._spawn(samples[r_start_index:r_end_index])
	extract.export(f"Samples/{instrument}/{mute}/Sound/Release/{file_name}_Release.wav", format="wav")
	

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

sample(sound)
# Sustain, then
# Attack, then
# End
