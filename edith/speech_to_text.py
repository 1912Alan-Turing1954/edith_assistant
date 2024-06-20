from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="facebook/seamless-m4t-v2-large")

# Path to your audio file
audio_file = "data/dialogue/dialogue_1_copy.wav"

# Perform speech-to-text
transcription = pipe(audio_file)

print("Transcription:", transcription)

# import pyaudio
# import wave
# from transformers import pipeline

# # Initialize the ASR pipeline using the specified model
# pipe = pipeline("automatic-speech-recognition", model="facebook/seamless-m4t-v2-large")

# # Function to capture audio from the microphone
# def capture_audio():
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 16000
#     RECORD_SECONDS = 5  # Adjust as needed

#     audio = pyaudio.PyAudio()

#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)

#     print("Listening...")

#     frames = []

#     for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     # Save audio to a file (optional)
#     wf = wave.open("microphone_input.wav", 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(audio.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()

#     return b''.join(frames)

# # Function to transcribe speech from microphone input
# def transcribe_microphone():
#     audio_data = capture_audio()

#     # Perform speech-to-text using the pipeline
#     transcription = pipe(audio_data)

#     return transcription

# if __name__ == "__main__":
#     # Perform transcription from microphone
#     result = transcribe_microphone()
#     print("Transcription:", result)
