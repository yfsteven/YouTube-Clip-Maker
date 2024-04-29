import requests, re, os, json, sys, datetime
from pytube import YouTube
from moviepy.editor import *

url = input('Input a YouTube Link\n')

re_strip_url = re.compile(r'https://www.youtube.com/(.*)?v=(.*)')

video_id = ""
os.makedirs('youtube_folder', exist_ok=True)

is_there_anything = re_strip_url.findall(str(url))

if len(is_there_anything) > 0:
    video_id = re_strip_url.search(str(url)).group(2)
else:
    print("Can't do. Link is probably invalid")
    sys.exit()

most_replayed_data = json.loads(requests.get(f"https://yt.lemnoslife.com/videos?part=mostReplayed&id={video_id}").text)

check_availablereplayed = most_replayed_data['items'][0]['mostReplayed']

if check_availablereplayed == None:
    print(f"Video {url} doesn't has most replayed data available")
    sys.exit()
else:
    print("Success!!!")

marker_data = check_availablereplayed['markers']

high_intense_moments = []

for i in range(len(marker_data)):
    if marker_data[i]['intensityScoreNormalized'] >= 0.5 and marker_data[i]['startMillis'] != 0:
        high_intense_moments.append(marker_data[i]['startMillis'])

if len(high_intense_moments) > 0:
    print(high_intense_moments)
    print("Clip worthy")
else:
    print("Nothing interesting")
    sys.exit()

converted_to_seconds = []
"""
yt = YouTube(url)

yd = yt.streams.get_highest_resolution()

yd.download("./youtube_folder/")

"""

short_width = 1080
short_height = 1920
