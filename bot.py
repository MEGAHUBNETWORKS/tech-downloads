import os
import requests
import asyncio
import random
import edge_tts
import PIL.Image
import json

# --- IMAGE FIX ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- CREDENTIALS ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"
PEXELS_API = os.getenv('PEXELS_API_KEY')
IG_USER = "zaindevilxq2"
IG_PASS = "zain@zain123"

async def create_video():
    print("🎬 Creating Viral Gaming Clip...")
    headers = {"Authorization": PEXELS_API}
    res = requests.get("https://api.pexels.com/videos/search?query=gaming&per_page=15", headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Adding AI Voiceover...")
    txt = "Free 100 dollar steam card at rewards hub. Link in bio now!"
    await edge_tts.Communicate(txt, "en-US-GuyNeural").save("voice.mp3")

    clip = VideoFileClip("raw.mp4").subclip(0, 15).resize(height=1920).crop(x_center=540, width=1080)
    final = clip.set_audio(AudioFileClip("voice.mp3"))
    final.write_videofile("final.mp4", fps=30, codec="libx264", audio_codec="aac")

def post_to_youtube():
    try:
        print("📺 Uploading YouTube Short...")
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"Get $100 Steam Credit FREE {random.randint(2025, 2026)}")
        video.set_description(f"CLAIM HERE: {LINK}")
        video.set_category(20) # 20 = Gaming
        video_info = channel.upload_video(video)
        
        # Pinned Comment
        channel.comment_on_video(video_info.id, f"🎁 GET YOUR $100 GIFT CARD HERE ➡️ {LINK}")
        print("✅ YouTube Success & Pinned")
    except Exception as e: print(f"❌ YouTube Error: {e}")

def post_to_instagram():
    try:
        print("📲 Connecting to Instagram...")
        cl = Client()
        session_file = "ig_session.json"
        
        if os.path.exists(session_file):
            cl.load_settings(session_file)
        
        cl.login(IG_USER, IG_PASS)
        cl.dump_settings(session_file) # Save session for next time
        
        cl.video_upload("final.mp4", caption=f"FREE $100! 🚀 Link in Bio! #gaming #free")
        print("✅ Instagram Success")
    except Exception as e: print(f"❌ Instagram Error: {e}")

async def run():
    await create_video()
    post_to_youtube()
    post_to_instagram()

if __name__ == "__main__":
    asyncio.run(run())

