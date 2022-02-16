import pyaudio
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "file.wav"

stop_ = False
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Start to record the audio.")

def stop():
    global stop_
    while True:
        if not input('Press Enter >>>'):
            print('exit')
            stop_ = True


t = threading.Thread(target=stop, daemon=True).start()
frames = []

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    if stop_:
        break

stream.stop_stream()
stream.close()
audio.terminate()
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()