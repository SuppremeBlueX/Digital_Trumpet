from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"

file_name = input("File name: ")


def sample_sustain(sound):
	extract = sound[1000:1050] # difference of about 10x wavelength
	extract.export(f"Samples/{instrument}/{mute}/Sound/Test_{file_name}_Sustain", format="wav")
	return None
	
def sample_attack(sound_file):
	extract = sound[0:200]
	extract.export(f"Samples/{instrument}/{mute}/Sound/Test_{file_name}_Attack", format="wav")
	return None

def sample_release(sound_file):
	extract = sound[-200:-1]
	extract.export(f"Samples/{instrument}/{mute}/Sound/Test_{file_name}_Release", format="wav")
	return None

# -----------------------------------------------------------------------------------------------

sound = AudioSegment.from_wav(f"Samples/{instrument}/{mute}/Sound/{file_name}")

sample_sustain(sound)
sample_attack(sound)
sample_release(sound)

# Sustain, then
# Attack, then
# End
