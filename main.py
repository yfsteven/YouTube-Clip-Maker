import requests, re, os, json, sys, time
from pytube import YouTube
from moviepy.editor import *
from transcribe_anything.api import transcribe
from moviepy.video.fx.all import crop
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

url = input('Input a YouTube Link\n')

re_strip_url = re.compile(r'https://www.youtube.com/(.*)?v=(.*)')

video_id = ""

os.makedirs('youtube_folder', exist_ok=True)
os.makedirs('clip_folder', exist_ok=True)
os.makedirs('processed_folder', exist_ok=True)

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

yt = YouTube(url)

title = yt.title

yd = yt.streams.get_highest_resolution()

yd.download(f"./youtube_folder/", filename=f"{title}")

short_width = 1080
short_height = 1920

clip_list = []
processed_clips = []

for start in converted_high_intense_moments:
        end = converted_high_intense_moments[start]

        clip = VideoFileClip(f'./youtube_folder/{title}').subclip(start, end)

        resized_clip = clip.resize(height=short_height)

        new_clip = crop(resized_clip, x_center=960, y_center=960, width=short_width, height=short_height)

        clip_list.append(os.path.join('./clip_folder/', f"{title}from{start}to{end}.mp4"))
        processed_clips.append(os.path.join('./processed_folder/', f"{title}from{start}to{end}.mp4"))

        new_clip.write_videofile(os.path.join('./clip_folder/', f"{title}from{start}to{end}.mp4"), audio=True, codec="libx264", threads=10)


for clip_path in clip_list:
    transcribe(
        url_or_file=clip_path,
        output_dir="./processed_folder",
    )


channel = Channel()
channel.login("client_secret.json", "credentials.storage")

for video in processed_clips:
    video = LocalVideo(file_path=f"{video}")

    video.set_title(title)
    video.set_description('Made by a bot')
    video.set_tags(["shorts"])
    video.set_category("education")
    video.set_default_language("en-US")


    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status("public")
    video.set_public_stats_viewable(True)

    video = channel.upload_video(video)

    video.like()
































