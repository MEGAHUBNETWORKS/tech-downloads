import os
import requests
import asyncio
import random
import edge_tts
from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

# --- CONFIGURATION ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
IG_SESSION = os.getenv('INSTAGRAM_SESSION_ID')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC" # Your Linkvertise

# Viral Voiceover Scripts
SCRIPTS = [
    "Stop scrolling! If you want a 100 dollar steam card for free, go to the link in my bio right now. It actually works!",
    "I just found a secret way to get premium gaming rewards for free. Check the link in my bio before it is patched!",
    "Want 100 dollars in your steam wallet? I just got mine from Rewards Hub. Link in my bio to start!"
]

async def create_video():
    print("🎥 Fetching viral gaming clip...")
    headers = {"Authorization": PEXELS_API}
    res = requests.get("https://api.pexels.com/videos/search?query=gaming&per_page=10", headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    with open("raw_video.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Generating AI Voiceover...")
    text = random.choice(SCRIPTS)
    communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
    await communicate.save("voice.mp3")

    print("🎬 Finalizing Video...")
    video = VideoFileClip("raw_video.mp4").subclip(0, 10).resize(height=1920).crop(x_center=540, width=1080)
    voice = AudioFileClip("voice.mp3")
    
    # Mix audio
    final_video = video.set_audio(voice)
    final_video.write_videofile("final_post.mp4", fps=24, codec="libx264", audio_codec="aac")

def post_to_instagram():
    print("📲 Posting to Instagram...")
    cl = Client()
    cl.set_settings({"sessionid": IG_SESSION})
    
    caption = f"GET $100 REWARDS NOW! 🚀\n.\n🔗 LINK IN BIO: {LINK}\n.\n#gaming #steam #freebie #pcgaming #rewardshub"
    cl.video_upload("final_post.mp4", caption=caption)
    print("✅ SUCCESS: Video is Live!")

if __name__ == "__main__":
    asyncio.run(create_video())
    post_to_instagram()
