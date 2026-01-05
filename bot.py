import os
import requests
import asyncio
import random
import edge_tts
import PIL.Image

# --- THE CRITICAL FIX FOR IMAGING ERRORS ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- CONFIGURATION & SEO ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"
PEXELS_API = os.getenv('PEXELS_API_KEY')
IG_SESSION = os.getenv('INSTAGRAM_SESSION_ID')
PINTEREST_TOKEN = os.getenv('PINTEREST_TOKEN')

# Viral Content Strategy: High-engagement scripts
SCRIPTS = [
    "Stop scrolling! You can get a hundred dollar steam card right now. Check the link in my bio.",
    "Gaming just got cheaper. I found a way to get free steam credit instantly. Link in my bio to try it.",
    "Need new games? Grab a free hundred dollar gift card at Rewards Hub. Don't wait, link in bio!"
]

async def create_trending_video():
    print("🎬 Fetching 4K Realistic Gaming Visuals...")
    headers = {"Authorization": PEXELS_API}
    query = random.choice(['gaming', 'pc gaming', 'ps5 gameplay', 'cyberpunk 2077'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=40"
    
    res = requests.get(url, headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Generating Realistic AI Voiceover...")
    text = random.choice(SCRIPTS)
    communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
    await communicate.save("voice.mp3")

    print("✂️ Mastering 15s Vertical Video...")
    clip = VideoFileClip("raw.mp4").subclip(0, 15)
    # Target 9:16 aspect ratio for Shorts/Reels/Pins
    clip = clip.resize(height=1920).crop(x_center=540, width=1080)
    
    voice = AudioFileClip("voice.mp3")
    final = clip.set_audio(voice)
    final.write_videofile("final.mp4", fps=30, codec="libx264", audio_codec="aac")

def post_to_youtube():
    try:
        print("📺 Uploading to YouTube Shorts...")
        channel = Channel()
        # Uses the files you uploaded to GitHub
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"How to get $100 Steam Credit FREE {random.randint(2025, 2026)}")
        video.set_description(f"GET YOURS HERE: {LINK}\n#gaming #shorts #free #steam")
        video.set_category("Gaming")
        video.set_keywords(["gaming", "shorts", "free", "steam", "money"])
        
        channel.upload_video(video)
        print("✅ YouTube Success")
    except Exception as e:
        print(f"❌ YouTube Error: {e}")

def post_to_instagram():
    try:
        print("📲 Posting to Instagram Reels...")
        cl = Client()
        cl.set_settings({"sessionid": IG_SESSION})
        caption = f"FREE $100 STEAM CREDIT! 🚀 Claim here: {LINK} #gaming #rewards #reels"
        cl.video_upload("final.mp4", caption=caption)
        print("✅ Instagram Success")
    except Exception as e:
        print(f"❌ Instagram Error: {e}")

def post_to_pinterest():
    # Placeholder for Pinterest API integration
    print("📌 Pinterest Hub: Post triggered for scheduling.")

async def run_engine():
    await create_trending_video()
    post_to_youtube()
    post_to_instagram()
    post_to_pinterest()

if __name__ == "__main__":
    asyncio.run(run_engine())

