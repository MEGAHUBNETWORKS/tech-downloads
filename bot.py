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
CAPTION = f"FREE $100 STEAM CREDIT! 🚀 Claim here: {LINK} #gaming #rewards"

async def create_video():
    print("🎥 Fetching video from Pexels...")
    headers = {"Authorization": PEXELS_API}
    # Added a check to see if API key exists
    if not PEXELS_API:
        print("❌ ERROR: PEXELS_API_KEY is missing in GitHub Secrets!")
        return False

    url = "https://api.pexels.com/videos/search?query=gaming&per_page=15"
    response = requests.get(url, headers=headers)
    res = response.json()

    if 'videos' not in res:
        print(f"❌ PEXELS API ERROR: {res}")
        return False

    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    print(f"📥 Downloading: {video_url}")
    with open("video.mp4", 'wb') as f:
        f.write(requests.get(video_url).content)

    print("🎙️ Generating Voiceover...")
    txt = "Stop scrolling! Get a 100 dollar steam card for free at Rewards Hub. Link in bio!"
    await edge_tts.Communicate(txt, "en-US-GuyNeural").save("voice.mp3")

    print("🎬 Editing Video...")
    clip = VideoFileClip("video.mp4").subclip(0, 10).resize(height=1920).crop(x_center=540, width=1080)
    clip = clip.set_audio(AudioFileClip("voice.mp3"))
    clip.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac")
    return True

def post_instagram():
    if not os.path.exists("final.mp4"):
        return
    try:
        print("📲 Posting to Instagram...")
        cl = Client()
        cl.set_settings({"sessionid": IG_SESSION})
        cl.video_upload("final.mp4", caption=CAPTION)
        print("✅ Instagram Posted!")
    except Exception as e:
        print(f"❌ Instagram Error: {e}")

async def main():
    success = await create_video()
    if success:
        post_instagram()

if __name__ == "__main__":
    asyncio.run(main())
