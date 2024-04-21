import speech_recognition as sr
from pytube import YouTube
import os
from moviepy.editor import *


def download_youtube_audio(youtube_url, output_path):
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Select the best audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream to a temporary file
    audio_stream.download(filename='temp_audio.mp4')

    # Convert the downloaded file to FLAC
    clip = AudioFileClip('temp_audio.mp4')
    clip.write_audiofile(output_path, codec='flac')  # Specify codec explicitly

    # Remove the temporary MP4 file
    os.remove('temp_audio.mp4')


def transcribe_audio(audio_file):
    # Initialize recognizer
    r = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    # Convert speech to text
    text = r.recognize_google(audio)

    return text


# Split into 10-second chunks by default
def split_audio_file(audio_file, chunk_length=10):
    audio = AudioFileClip(audio_file)
    audio_duration = audio.duration
    chunks = []
    for i in range(0, int(audio_duration), chunk_length):
        chunk = audio.subclip(i, min(i + chunk_length, audio_duration))
        chunk_file = f"chunk_{i}.flac"
        chunk.write_audiofile(chunk_file, codec='flac')
        chunks.append(chunk_file)
    return chunks


youtube_url = "https://youtu.be/sJBO7rMR8ks"
output_path = 'output_file.flac'
download_youtube_audio(youtube_url, output_path)

# Split the audio file into segments
chunks = split_audio_file(output_path)

# Transcribe each segment and combine the results
transcribed_text = ""
for chunk in chunks:
    transcribed_text += transcribe_audio(chunk)

# Print the transcribed text
print("\nThe resultant text from the video is:\n")
print(transcribed_text)
