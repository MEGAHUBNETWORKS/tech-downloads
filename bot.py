import os
import requests
import asyncio
import random
import edge_tts
import PIL.Image

# --- IMAGE FIX ---
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

from moviepy.editor import VideoFileClip, AudioFileClip, vfx, CompositeAudioClip
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- SETTINGS ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"
PEXELS_API = os.getenv('PEXELS_API_KEY')

async def create_hype_video():
    print("🎬 Fetching High-Action Gameplay...")
    headers = {"Authorization": PEXELS_API}
    # Using high-energy search terms
    query = random.choice(['parkour', 'gta v stunts', 'fast racing', 'minecraft drop'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15"
    res = requests.get(url, headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Generating Hype Voiceover...")
    # Fast, aggressive script for high retention
    txt = "WAIT! 🛑 Don't skip! You want a hundred dollar gift card for FREE? I just got mine at the link in my description! Go now before it expires! 🚀"
    await edge_tts.Communicate(txt, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    print("🎵 Adding Music & Zoom Effects...")
    clip = VideoFileClip("raw.mp4").subclip(0, 10).resize(height=1920).crop(x_center=540, width=1080)
    
    # Simple zoom effect: Start slightly larger and "shake" or mirror
    if random.random() > 0.5:
        clip = clip.fx(vfx.mirror_x)

    # Royalty-free high-energy music
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
    
    voice = AudioFileClip("voice.mp3")
    bg_music = AudioFileClip("bg.mp3").volumex(0.12).set_duration(voice.duration)
    
    final_audio = CompositeAudioClip([voice, bg_music])
    final = clip.set_audio(final_audio)
    final.write_videofile("final.mp4", fps=30, codec="libx264", audio_codec="aac")

def post_to_youtube():
    try:
        print("📺 Uploading High-Energy Short...")
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"FREE $100 GIFT CARD! 🎁 #shorts #gaming")
        video.set_description(f"GET IT HERE: {LINK}")
        video.set_category(20)
        
        video_info = channel.upload_video(video)
        print(f"✅ YouTube Success! Video ID: {video_info.id}")
    except Exception as e:
        print(f"❌ YouTube Error: {e}")

async def main():
    await create_hype_video()
    post_to_youtube()
    # Instagram is paused until you click 'This was me' on your phone's login alert.

if __name__ == "__main__":
    asyncio.run(main())
