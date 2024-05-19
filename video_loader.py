import os
from pytube import YouTube
from pydub import AudioSegment

def Download(link):
    # Initialize YouTube object
    youtubeObject = YouTube(link)
    
    # Filter streams to get only audio
    audio_stream = youtubeObject.streams.filter(only_audio=True).first()
    
    try:
        # Download audio file
        download_path = audio_stream.download()
        
        # Convert downloaded file to MP3
        base, ext = os.path.splitext(download_path)
        mp3_path = base + '.mp3'
        
        # Convert to mp3 using pydub
        audio = AudioSegment.from_file(download_path)
        audio.export(mp3_path, format='mp3')
        
        # Remove the original downloaded file
        os.remove(download_path)
        
        return f"Download and conversion complete: {mp3_path}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    print(Download(link))
