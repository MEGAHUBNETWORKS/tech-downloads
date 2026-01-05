import os
import requests
import asyncio
import random
import edge_tts
import PIL.Image

# --- FIXES ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- CONFIG ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"
PEXELS_API = os.getenv('PEXELS_API_KEY')
# For Instagram: Use your actual credentials in GitHub Secrets
IG_USER = os.getenv('INSTAGRAM_USERNAME') 
IG_PASS = os.getenv('INSTAGRAM_PASSWORD')

SCRIPTS = [
    "Stop scrolling! You can get a hundred dollar steam card right now. Check the link in my bio.",
    "Gaming just got cheaper. I found a way to get free steam credit instantly. Link in my bio to try it.",
    "Need new games? Grab a free hundred dollar gift card at Rewards Hub. Don't wait, link in bio!"
]

async def create_trending_video():
    print("🎬 Fetching 4K Gaming Visuals...")
    headers = {"Authorization": PEXELS_API}
    query = random.choice(['gaming', 'ps5 gameplay', 'pc gaming'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=40"
    res = requests.get(url, headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Generating AI Voice...")
    text = random.choice(SCRIPTS)
    await edge_tts.Communicate(text, "en-US-GuyNeural").save("voice.mp3")

    print("✂️ Mastering 15s Vertical Video...")
    clip = VideoFileClip("raw.mp4").subclip(0, 15).resize(height=1920).crop(x_center=540, width=1080)
    final = clip.set_audio(AudioFileClip("voice.mp3"))
    final.write_videofile("final.mp4", fps=30, codec="libx264", audio_codec="aac")

def post_to_youtube():
    try:
        print("📺 Uploading to YouTube Shorts...")
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"How to get $100 Steam Credit FREE {random.randint(2025, 2026)}")
        video.set_description(f"GET YOURS HERE: {LINK}\n#gaming #shorts #free")
        video.set_category(20) # Fixed: 20 is the ID for Gaming
        
        video_info = channel.upload_video(video)
        video_id = video_info.id
        print(f"✅ YouTube Success: {video_id}")

        # Post Pinned Comment
        comment_text = f"🎁 CLAIM YOUR $100 GIFT CARD HERE ➡️ {LINK} (Limited Time!)"
        channel.comment_on_video(video_id, comment_text)
        print("📌 Comment Pinned!")
    except Exception as e: print(f"❌ YouTube Error: {e}")

def post_to_instagram():
    try:
        print("📲 Logging into Instagram...")
        cl = Client()
        # Direct login using Username and Password
        cl.login(IG_USER, IG_PASS)
        caption = f"FREE $100 STEAM CREDIT! 🚀 Claim here: {LINK} #gaming #rewards"
        cl.video_upload("final.mp4", caption=caption)
        print("✅ Instagram Success")
    except Exception as e: print(f"❌ Instagram Error: {e}")

async def main():
    await create_trending_video()
    post_to_youtube()
    post_to_instagram()

if __name__ == "__main__":
    asyncio.run(main())
