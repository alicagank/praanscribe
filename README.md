# praanscribe

praanscribe is a small application for automatically transcribing audio and creating TextGrid files to be used in Praat.

## Purpose

Praat utilizes the ‘TextGrid’ file format to integrate annotations into audio files. Manual transcription is frequently utilized during this process. The application’s goal is to automate this procedure by transcribing the utterances from audio files and generating TextGrid files that match the original audio’s length.

## Usage

```bash
python praanscribe.py
```

- `<language_code>`: Language code indicating the language of the audio such as 'en', 'tr', 'fr', or more specific dialects like 'en-US', 'tr-TR', etc.
- `<audio_file>`: Path to the audio file (.wav) you want to transcribe.


The output is a simple TextGrid file where each word has the same length, stretching through the duration of the audio. This file, along with the audio can be further edited and analyzed using Praat.
