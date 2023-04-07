import argparse

parser = argparse.ArgumentParser(description='Download a file.')
parser.add_argument('url', help='the URL to download')
parser.add_argument('mp3_name', help='the name of the mp3 file')
args = parser.parse_args()

if not args.url:
    print('No URL provided')
    exit()

import os
from pytube import YouTube

os.makedirs('static/downloads', exist_ok=True)

mp3_name = args.mp3_name
def main(url):
    mp4_file = f'{mp3_name}.mp4'

    video = YouTube(url)
    streams = video.streams.filter(only_audio=True)
    streams.first().download(filename=mp4_file)

    cmd = f'ffmpeg -y -i {mp3_name}.mp4 -af asetrate=44100*1.75,aresample=44100,atempo=1/1.75 -c:a libmp3lame "static/downloads/first-{mp3_name}.mp3"'
    print(cmd)
    os.system(cmd)
    
    cmd = f'ffmpeg -y -i "static/downloads/first-{mp3_name}.mp3" -c:a libmp3lame "static/downloads/{mp3_name}.mp3"'
    print(cmd)
    os.system(cmd)

    os.remove(f"static/downloads/first-{mp3_name}.mp3")
    os.remove(mp4_file)

main(args.url)