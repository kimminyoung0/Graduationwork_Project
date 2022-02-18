from flask import Flask, render_template
import pyaudio
import wave
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("webh.html")

# @webserver.route('/execute')
# def exe():
#     return //음성녹음이 실행되는 html을 넣어야 하나..?

if __name__ == '__main__' :
    app.run(debug = True)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Start to record the audio.")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

key = '459bf05a19af805c9f415f7523b0e7a4'

headers = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK " + key,
}

with open('./file.wav', 'rb') as fp:
    audio = fp.read()

res = requests.post(kakao_speech_url, headers=headers, data=audio)
print(res.text)

result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
result = json.loads(result_json_string)
print(result)
print(result['value'])