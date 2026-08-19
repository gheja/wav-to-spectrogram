import wav_to_spectrogram as wts

wts.wav_to_spectrogram("audio.wav", "spectrogram_fullscreen.png", 1920, 1080)
wts.wav_to_spectrogram_video("audio.wav", "spectrogram.mp4", 1920, 80, 25)
