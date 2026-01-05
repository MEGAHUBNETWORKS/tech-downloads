import os
import requests
import asyncio
import random
import edge_tts
from instagrapi import Client
from moviepy.editor import VideoFileClip, AudioFileClip

# --- CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
IG_SESSION = os.getenv('INSTAGRAM_SESSION_ID')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

async def create_video():
    print("🎥 Fetching video...")
    headers = {"Authorization": PEXELS_API}
    url = "https://api.pexels.com/videos/search?query=gaming&per_page=15"
    res = requests.get(url, headers=headers).json()

    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    with open("video.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Generating Voiceover...")
    txt = "Stop scrolling! Get a 100 dollar steam card for free at Rewards Hub. Link in bio!"
    await edge_tts.Communicate(txt, "en-US-GuyNeural").save("voice.mp3")

    print("🎬 Finalizing Video...")
    # We remove the .resize() and use a simpler crop/set_duration to avoid Pillow errors
    clip = VideoFileClip("video.mp4").subclip(0, 10)
    voice = AudioFileClip("voice.mp3")
    
    final_video = clip.set_audio(voice)
    # This 'temp_audio_file' line fixes a common permission error in GitHub Actions
    final_video.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
    return True

def post_instagram():
    try:
        print("📲 Posting to Instagram...")
        cl = Client()
        cl.set_settings({"sessionid": IG_SESSION})
        caption = f"FREE $100 STEAM CREDIT! 🚀 Claim here: {LINK} #gaming #rewards"
        cl.video_upload("final.mp4", caption=caption)
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Instagram Error: {e}")

async def main():
    if await create_video():
        post_instagram()

if __name__ == "__main__":
    asyncio.run(main())
