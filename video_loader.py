import os
from pytube import YouTube
from moviepy.editor import AudioFileClip

def Download(link):
    # Initialize YouTube object
    youtubeObject = YouTube(link)
    
    # Filter streams to get only audio
    audio_stream = youtubeObject.streams.filter(only_audio=True).first()
    
    try:
        # Download audio file
        download_path = audio_stream.download()
        
        # Convert downloaded file to MP3 using moviepy
        base, ext = os.path.splitext(download_path)
        mp3_path = base + '.mp3'
        
        # Load the audio file
        audio_clip = AudioFileClip(download_path)
        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()
        
        # Remove the original downloaded file
        os.remove(download_path)
        
        return mp3_path
    except Exception as e:
        return 1

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    print(Download(link))
