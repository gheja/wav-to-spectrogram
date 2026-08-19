import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import subprocess
import os

def wav_to_spectrogram(input_wav, output_png, width = 1920, height = 1080, ax_nfft = 2048, ax_noverlap = 1024):
	print("Reading audio...")
	sample_rate, audio = wavfile.read(input_wav)
	
	print("Processing audio...")
	# any number of channels -> mono
	if audio.ndim > 1:
		audio = audio.mean(axis=1)
	
	audio = audio.astype(np.float32)
	
	duration = len(audio) / sample_rate
	
	print("Creating spectrogram...")
	
	fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
	
	ax = fig.add_axes([0, 0, 1, 1])
	
	ax.specgram(
		audio,
		Fs=sample_rate,
		NFFT=ax_nfft,
		noverlap=ax_noverlap,
		cmap="magma"
	)
	
	ax.set_ylim(0, 22_000)
	
	ax.axis("off")
	
	fig.savefig(
		output_png,
		dpi=100,
		bbox_inches=None,
		pad_inches=0
	)
	
	plt.close(fig)
	
	print(f"Image created: {output_png}")

	return duration

def wav_to_spectrogram_video(input_wav, output_mp4, width = 1920, height = 1080, fps = 60, ax_nfft = 2048, ax_noverlap = 1024):
	tmp_image = "spectrogram_tmp.png"

	duration = wav_to_spectrogram(input_wav, tmp_image, width, height, ax_nfft, ax_noverlap)
	
	print("Rendering video...")
	
	command = [
		"ffmpeg",
	
		# loop the static spectrogram image
		"-loop", "1",
		"-i", tmp_image,
		
		# background for the playhead line
		"-f",  "lavfi", "-i", f"color=c=white:s=3x1080:r={fps}:d={duration}",
	
		# input audio
		"-i", input_wav,
	
		# combining final video
		"-filter_complex", f"[1:v]drawbox=x=0:y=0:w=3:h=ih:color=white@1:t=fill[line];[0:v][line]overlay=x='(W-w)*t/{duration}':y=0:format=auto",
		"-r", str(fps),
	
		"-c:v", "libx264", "-preset", "faster", "-crf", "18",
		"-pix_fmt", "yuv420p", "-movflags", "faststart",
	
		"-c:a", "aac", "-b:a", "192k",
	
		"-shortest",
		
		"-y",
		output_mp4
	]
	
	subprocess.run(command, check=True)
	
	print(f"Cleaning up temp image {tmp_image}...")
	os.remove(tmp_image)
	
	print(f"Video created: {output_mp4}")

