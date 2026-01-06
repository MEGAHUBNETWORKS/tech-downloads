import warnings
import os, asyncio, random, requests, datetime, time
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY') 
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def apply_realistic_grading(image):
    """Natural Realistic Grading: Enhances detail without the 'Teal' look."""
    img = image.astype(float)
    # Balanced contrast enhancement for realistic animations
    img *= 1.05 
    return np.clip(img, 0, 255).astype('uint8')

def apply_impact_vfx(image, t, impact_start, impact_end):
    """Realistic impact shake for animations."""
    if impact_start <= t <= impact_end:
        shift = random.randint(-40, 40)
        image = np.roll(image, shift, axis=0) 
    return apply_realistic_grading(image)

async def produce_and_upload():
    try:
        if not os.path.exists("credentials.storage"):
            print("❌ STOP: credentials.storage missing.")
            return

        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")

        # --- AI ANIMATION SELECTION ---
        # Targeting realistic national animations and high-end CGI
        niche_query = random.choice([
            'realistic 3d animation 4k',
            'national geographic style CGI nature',
            'realistic architectural animation',
            'cinematic 3d environment 4k'
        ])
        
        headers = {"Authorization": PEXELS_API}
        res = requests.get(f"https://api.pexels.com/videos/search?query={niche_query}&per_page=15&orientation=portrait&min_duration=10", headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
        
        with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

        # --- PRODUCTION ---
        raw_clip = VideoFileClip("raw.mp4").resize(height=1920).crop(x_center=540, width=1080)
        target_dur = min(raw_clip.duration, 9.0)
        mid = target_dur / 2
        
        c1 = raw_clip.subclip(0, mid - 0.7).fx(vfx.speedx, 1.5)
        c2 = raw_clip.subclip(mid - 0.7, mid + 0.8).fx(vfx.speedx, 0.5) 
        c3 = raw_clip.subclip(mid + 0.8, target_dur).fx(vfx.speedx, 2.0)
        clip = concatenate_videoclips([c1, c2, c3])
        
        imp_start = (mid - 0.7) / 1.5
        imp_end = imp_start + (1.5 / 0.5)
        clip = clip.fl(lambda gf, t: apply_impact_vfx(gf(t), t, imp_start, imp_end))

        # --- EXPORT & UPLOAD ---
        audio = AudioFileClip("audio.mp3").set_duration(clip.duration).volumex(2.5)
        final = CompositeVideoClip([clip]).set_audio(audio)
        
        final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"REALIS
        TIC ANIMATION 4K // {datetime.date.today()} #animation #realistic #4k")
        video.set_description(f"UNLIMITED ACCESS: {LINK}")
        uploaded = channel.upload_video(video)
        print(f"🚀 GLOBAL DEPLOY: https://youtu.be/{uploaded.id}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(produce_and_upload())
