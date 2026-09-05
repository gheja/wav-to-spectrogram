import sys
import os
import wav_to_spectrogram as wts

input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0] + ".mp4"

if os.path.exists(output_file):
    print(f"{output_file}: file exist, aborting.")
    sys.exit(1)

wts.wav_to_spectrogram_video(input_file, output_file, 800, 200, 25)
