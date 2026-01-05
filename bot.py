import os
import requests
import asyncio
import random
import edge_tts
import PIL.Image

# Fix for the Pillow error
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- CONFIG ---
PEXELS_API = "HRXjc3NHm3XeqDYCYZEECFUaROWc7zgK3uUxxJkEphgmd8VURheTUI7r"
IG_SESSION = os.getenv('INSTAGRAM_SESSION_ID')
PINTEREST_TOKEN = os.getenv('PINTEREST_TOKEN')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

async def create_realistic_video():
    print("🎬 Fetching 4K Gaming Clip...")
    headers = {"Authorization": PEXELS_API}
    res = requests.get("https://api.pexels.com/videos/search?query=gaming&per_page=20", headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Adding Realistic AI Voice...")
    txt = "Stop scrolling! Get a 100 dollar steam card for free at Rewards Hub. Link in bio!"
    await edge_tts.Communicate(txt, "en-US-GuyNeural").save("voice.mp3")

    print("✂️ Mastering 15s Vertical Video...")
    clip = VideoFileClip("raw.mp4").subclip(0, 15).resize(height=1920).crop(x_center=540, width=1080)
    final = clip.set_audio(AudioFileClip("voice.mp3"))
    final.write_videofile("final.mp4", fps=30, codec="libx264", audio_codec="aac")

def post_all():
    # INSTAGRAM
    try:
        cl = Client()
        cl.set_settings({"sessionid": IG_SESSION})
        cl.video_upload("final.mp4", caption=f"CLAIM $100! 🚀 Link in Bio! #gaming")
        print("✅ Instagram Posted")
    except Exception as e: print(f"❌ IG Error: {e}")

    # YOUTUBE
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        video = LocalVideo(file_path="final.mp4")
        video.set_title("Free $100 Steam Credit 2026")
        channel.upload_video(video)
        print("✅ YouTube Posted")
    except Exception as e: print(f"❌ YouTube Error: {e}")

async def main():
    await create_realistic_video()
    post_all()

if __name__ == "__main__":
    asyncio.run(main())

