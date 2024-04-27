import speech_recognition as sr
import wave
import sys
import os

def transcribe_audio(audio_file, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        # Language code provided by the user
        transcript = recognizer.recognize_google(audio_data, language=language)
        return transcript.split()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def get_audio_duration(audio_file):
    with wave.open(audio_file, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

def get_equal_duration(timestamps, total_duration):
    num_words = len(timestamps)
    return total_duration / num_words

def get_timestamps_with_equal_duration(words, total_duration):
    duration_per_word = get_equal_duration(words, total_duration)
    timestamps = []
    start_time = 0
    for word in words:
        end_time = start_time + duration_per_word
        timestamps.append((word, start_time, end_time))
        start_time = end_time
    return timestamps

def write_to_textgrid(output_file, timestamps):
    with open(output_file, "w") as file:
        file.write("File type = \"ooTextFile\"\n")
        file.write("Object class = \"TextGrid\"\n\n")
        file.write("xmin = 0\n")
        file.write(f"xmax = {timestamps[-1][2]}\n")
        file.write("tiers? <exists>\n")
        file.write("size = 1\n")
        file.write("item []:\n")
        file.write("    item [1]:\n")
        file.write("        class = \"IntervalTier\"\n")
        file.write("        name = \"words\"\n")
        file.write("        xmin = 0\n")
        file.write(f"        xmax = {timestamps[-1][2]}\n")
        file.write("        intervals: size = {}\n".format(len(timestamps)))
        for i, (word, start_time, end_time) in enumerate(timestamps, start=1):
            file.write(f"        intervals [{i}]:\n")
            file.write(f"            xmin = {start_time}\n")
            file.write(f"            xmax = {end_time}\n")
            file.write(f"            text = \"{word}\"\n")

def print_help():
    print("praanscribe")
    print("A small application for automatically transcribing audio and creating TextGrid files to be used in Praat.")
    print("\nUsage:")
    print("python praanscribe.py")
    print("\nOutput:")
    print("The output is a simple TextGrid file where each word has the same length, stretching through the duration of the audio. This file can be further edited and analyzed using Praat.")

def prompt_for_input():
    language_code = input("Enter the language code (e.g., 'en', 'tr'): ")
    audio_file = input("Enter the path to the audio file: ")
    return language_code, audio_file

def run_again():
    answer = input("Run again? (yes/no): ").strip().lower()
    return answer == '' or answer == 'yes'

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    while True:
        print_help()
        language_code, audio_file = prompt_for_input()
        output_file = os.path.join(script_directory, os.path.splitext(os.path.basename(audio_file))[0] + ".TextGrid")
        words = transcribe_audio(audio_file, language=language_code)
        if words:
            total_duration = get_audio_duration(audio_file)
            timestamps = get_timestamps_with_equal_duration(words, total_duration)
            write_to_textgrid(output_file, timestamps)
            print(f"TextGrid file saved: {output_file}")
        if not run_again():
            break