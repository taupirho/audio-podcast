import base64
import json
import os
import re
import requests
import shutil
import argparse
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize argument parser
parser = argparse.ArgumentParser(description='Generate podcast audio with elevenlabs TTS services')
parser.add_argument(
    '--tts_service', 
    choices=['elevenlabs'], 
    default='elevenlabs', 
    help='Choose TTS service: elevenlabs'
)
parser.add_argument(
    '--input_file', 
    required=True, 
    help='Path to the input file containing the podcast text'
)

parser.add_argument(
    '--output_file', 
    default='podcast.mp3', 
    help='Path to the output merged audio file (default: podcast.mp3)'
)

def synthesize_elevenlabs(text, speaker, global_index, turn_index):
    """ElevenLabs TTS synthesis"""
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    
    # Map speakers to ElevenLabs voice IDs
    voice_mapping = {
        'Alice': "123456789",  
        'Bob': "987654321"  
    }
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_mapping[speaker]}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }
    
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.text}")
        raise Exception("Failed to fetch audio from ElevenLabs")
    
    filename = f"audio-files/{global_index:03d}_{turn_index:03d}_{speaker}.mp3"
    with open(filename, "wb") as out:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)
    
    return filename

def generate_audio(conversation, tts_service='elevenlabs'):
    """Generate audio using specified TTS service"""
    if not os.path.exists('audio-files'):
        os.makedirs('audio-files')
    else:
        for file in os.listdir('audio-files'):
            os.remove(os.path.join('audio-files', file))
    
    audio_files = []
    
    for i, turn in enumerate(conversation):
      if tts_service == 'elevenlabs':
            filename = synthesize_elevenlabs(turn['text'], turn['speaker'], 0, i)
      else:
            raise ValueError(f"Unknown TTS service: {tts_service}")
            
      audio_files.append(filename)
    
    return sorted(audio_files)

def merge_audios(audio_files, output_file):
    """Merge multiple audio files into one"""
    combined = AudioSegment.empty()
    
    for audio_file in audio_files:
        print(f"Processing: {audio_file}")
        audio = AudioSegment.from_file(audio_file)
        combined += audio
        
    combined.export(output_file, format="mp3")
    print(f"Merged audio saved as {output_file}")

def main():
    args = parser.parse_args()
    
    with open(args.input_file, 'r') as file:
        conversation = json.load(file)
    
    audio_files = generate_audio(conversation, args.tts_service)
    merge_audios(audio_files, args.output_file)

if __name__ == "__main__":
    main()