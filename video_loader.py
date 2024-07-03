import os
from pytube import YouTube
from pytube import Search

def SearchQuery(query):
    s = Search(query)

    for item in s:
        print(item.title + " - " + item.author)
        print()

def Download(link):
    # Initialize YouTube object
    youtubeObject = YouTube(link)
    
    # Filter streams to get only audio
    audio_stream = youtubeObject.streams.filter(only_audio=True).first()
    
    try:
        # Download audio file
        download_path = audio_stream.download()
        base, ext = os.path.splitext(download_path)
        new_file = base + '.mp3'
        os.rename(download_path, new_file)
        
        return new_file
    except Exception as e:
        return False

if __name__ == "__main__":
    link = input("Enter the YouTube video URL: ")
    print(Download(link))
