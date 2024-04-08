from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"

def locate_peaks(sound):
	peak = 0
	peaks = []
	peaking = False
	samples = sound.get_array_of_samples()
	for index, sample in enumerate(samples):
		if index % 2 == 0:
			continue
		else:
			delta = samples[index] - samples[index-2] # delta change
			if sample > 0 and delta < 0:
				if peaking == False:
					peak += 1
					samples[index-2] = (2**15)-1
					peaks.append(index-2)
					peaking = True
			elif sample < 0 and peaking == True:
				peaking = False
	return samples, peaks
	
def find_indices(sound,peaks):
	start_index = None
	end_index = None
	max_amplitude = sound.max
	
	s_start_index = peaks[2000]
	s_end_index = peaks[2001]
	a_start_index = peaks[0]
	a_end_index = peaks[200]
	r_start_index = peaks[-100]
	r_end_index = peaks[-1]
	
	return s_start_index, s_end_index, a_start_index, a_end_index, r_start_index, r_end_index

def sample(sound):
	samples, peaks = locate_peaks(sound)
	print(len(peaks))
	s_start_index, s_end_index, a_start_index, a_end_index, r_start_index, r_end_index = find_indices(sound,peaks)
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
