import requests, re, os, json, sys
from pytube import YouTube
from moviepy.editor import *

url = input('Input a YouTube Link\n')

re_strip_url = re.compile(r'https://www.youtube.com/(.*)?v=(.*)')

video_id = ""

os.makedirs('youtube_folder', exist_ok=True)
os.makedirs('clip_folder', exist_ok=True)

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
    if marker_data[i]['intensityScoreNormalized'] >= 0.5 and marker_data[i]['startMillis'] != 0 and i != len(marker_data) - 1:
        high_intense_moments.append(marker_data[i]['startMillis'])

if len(high_intense_moments) > 0:
    print("Clip worthy")
else:
    print("Nothing interesting")
    sys.exit()

def convert_millisecond(ms):
    secs, ms = divmod(ms, 1000)
    mins, secs = divmod(secs, 60)
    return f"{int(mins):02d}:{int(secs):02d}"

converted_high_intense_moments = {convert_millisecond(i):convert_millisecond(i+30000) for i in high_intense_moments} # 30000 milisecond translates to 30 seconds

print(converted_high_intense_moments)

yt = YouTube(url)

title = yt.title

yd = yt.streams.get_highest_resolution()

yd.download(f"./youtube_folder/", filename=f"{title}")

short_width = 1080
short_height = 1920

for start in converted_high_intense_moments:
        end = converted_high_intense_moments[start]
        clip = VideoFileClip(f'./youtube_folder/{title}').subclip(start, end)
        clip.resize(height=1920)
        clip.crop(x_center=960, y_center=960, width=1080, height=1920)
        clip.write_videofile(os.path.join('./clip_folder/', f"{title}from{start}to{end}.mp4"), audio=True, codec="libx264", threads=10)
