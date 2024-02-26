from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"


def count_peaks_in_sample(percent):
	max_amplitude = sound.max
	#soundleft, soundright = sound.split_to_mono()
	samples = sound.get_array_of_samples()
	peaked = False
	peak = 0
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
	print(f"Number of Peaks within {percent*100}% of max amplitude in Sample: {peak}")
	return peak
	
def separate_by_peaks(sound, percent,peak_break):
	max_amplitude = sound.max
	samples = sound.get_array_of_samples()
	peaked = False
	peak = 0
	start_index = 0
	end_index = 0
	sustain_size = 0.1 # how long will the sound be held
	sustain_sample = 44100 * sustain_size # 44,100 khz * sound duration
	if peak_break > count_peaks_in_sample(percent):
		samples, start_index, end_index = separate_by_peaks(sound,percent-0.01,0)
	for index, sample in enumerate(samples):
		if sample >= (percent * max_amplitude): 
			print (peak, index, sample)
			samples[index] = min(sample*2,(2**15)-1)
			if peaked == False:   # the sound peaked
				peak = peak + 1
				peaked = True
				if peak == peak_break:
					start_index = index
				if (start_index > 0) and (index - start_index >= sustain_sample): # wait until start_index is set before checking for the end_index
					end_index = index
					break
		else:
			peaked = False
	#if end_index == 0:
	#	samples, start_index, end_index = separate_by_peaks(sound,percent,peak_break+1)
	return samples, start_index, end_index

def locate_peaks(sound):
	peak = 0
	peaks = []
	peaking = False
	max_amplitude = sound.max
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



def sample_sustain(sound):
	#samples, start_index, end_index = separate_by_peaks(sound,0.2,1)
	samples, peaks = locate_peaks(sound)
	print (len(peaks))
	extract = sound._spawn(samples[:]) # negate end because we're counting from the end
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

sample_sustain(sound)
sample_attack(sound)
sample_release(sound)
# Sustain, then
# Attack, then
# End
