from pydub import AudioSegment

instrument = "Bb_Trumpet"
mute = "Unmuted"

file_name = input("File name: ")

start = 0
end = 1500

sound = AudioSegment.from_wav(f"Samples/{instrument}/{mute}/Sound/{file_name}")
extract = sound[start:end]

extract.export(f"Samples/{instrument}/{mute}/Sound/sustained_{file_name}", format="wav")

# Sustain, then
# Attack, then
# End
