import warnings
# Fix the NameError by importing 'warnings' before using it
warnings.filterwarnings("ignore", category=FutureWarning)

import os, asyncio, random, math, requests, datetime, pickle, time
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY') 
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def apply_alpha_grading(image):
    """AI Teal & Orange: Cinematic Hollywood look."""
    img = image.astype(float)
    img[:, :, 0] *= 1.20  # Push Oranges
    img[:, :, 2] *= 1.18  # Push Teals
    return np.clip(img, 0, 255).astype('uint8')

def apply_kasmandra_vfx(image, t, impact_start, impact_end):
    """Aggressive screen shake and RGB split on impact."""
    if impact_start <= t <= impact_end:
        shift = random.randint(-55, 55)
        image = np.roll(image, shift, axis=0) 
        image[:, :, 0] = np.roll(image[:, :, 0], 25, axis=1) # Intense Chromatic Glitch
    return apply_alpha_grading(image)

async def produce_and_upload():
    try:
        # 1. AUTHENTICATION (The Unstuck Fix)
        if not os.path.exists("credentials.storage"):
            print("❌ STUCK PROTECT: credentials.storage missing. Create it locally first!")
            return

        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        print("✅ Logged in successfully via storage.")

        # 2. SELECT NICHE
        niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
        
        # 3. FETCH HIGH-DETAIL 4K ASSETS
        headers = {"Authorization": PEXELS_API}
        queries = {'JOHN_WICK': 'hitman combat 4k', 'FAST_FURIOUS': 'supercar drift 4k', 'MARVEL': 'superhero battle 4k'}
        res = requests.get(f"https://api.pexels.com/videos/search?query={queries[niche]}&per_page=15&orientation=portrait&min_duration=8", headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
        
        with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

        # 4. ADAPTIVE PRODUCTION (GTA 6 Style)
        raw_clip = VideoFileClip("raw.mp4").resized(height=1920).cropped(x_center=540, width=1080)
        target_dur = min(raw_clip.duration, 8.5)
        mid = target_dur / 2
        
        c1 = raw_clip.subclipped(0, mid - 0.7).with_effects([vfx.MultiplySpeed(1.8)])
        c2 = raw_clip.subclipped(mid - 0.7, mid + 0.8).with_effects([vfx.MultiplySpeed(0.4)]) # SLOW MO
        c3 = raw_clip.subclipped(mid + 0.8, target_dur).with_effects([vfx.MultiplySpeed(2.2)])
        clip = concatenate_videoclips([c1, c2, c3])
        
        imp_start = (mid - 0.7) / 1.8
        imp_end = imp_start + (1.5 / 0.4)

        # 5. VFX & 30k BITRATE EXPORT
        clip = clip.image_transform(lambda img, t: apply_kasmandra_vfx(img, t, imp_start, imp_end))
        
        # Use existing audio.mp3 or add downloader here
        audio = AudioFileClip("audio.mp3").with_duration(clip.duration).with_volume_scaled(3.5)
        
        final = CompositeVideoClip([clip]).with_audio(audio)
        final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

        # 6. UPLOAD
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"{niche} 💀 // 4K GTA 6 GRAPHICS #action #phonk")
        video.set_description(f"GET ACCESS: {LINK}")
        uploaded = channel.upload_video(video)
        print(f"🚀 GLOBAL DEPLOY SUCCESS: https://youtu.be/{uploaded.id}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

async def main():
    while True:
        await produce_and_upload()
        # Randomize wait between 3-5 hours to stay safe
        wait = random.randint(180, 300)
        print(f"💤 Sleeping for {wait} minutes. Next run at random interval...")
        await asyncio.sleep(wait * 60)

if __name__ == "__main__":
    asyncio.run(main())
        next_run = datetime.datetime.now() + datetime.timedelta(minutes=wait_time)
        print(f"💤 Sleeping. Next randomized upload at: {next_run.strftime('%H:%M:%S')}")
        await asyncio.sleep(wait_time * 60)

if __name__ == "__main__":
    asyncio.run(main_loop())

