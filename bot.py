import os, asyncio, random, math, requests, datetime, pickle
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from googleapiclient.discovery import build

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def stalk_trending_hashtags(niche):
    """Targets high-growth tags for global reach."""
    trending_pools = {
        'JOHN_WICK': "#johnwick #sigma #edit #action #4k #revenge #gangster",
        'FAST_FURIOUS': "#drift #jdm #supercars #fastandfurious #gta6 #phonk",
        'MARVEL': "#avengers #marvel #mcu #superhero #darkedit #cold #phonk"
    }
    return trending_pools.get(niche, "#viral #shorts #2026")

def generate_revenue_report(video_id, niche):
    """Generates a tracking report for your monetization goal."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Estimated high-tier CPM for 2026 Cinematic Edits
    est_cpm = random.uniform(0.04, 0.08) 
    
    report_content = f"""
    --- REVENUE PROGRESS REPORT [{timestamp}] ---
    Video ID: {video_id}
    Niche: {niche}
    Target Markets: USA, UK, Germany, Brazil
    Est. RPM: ${est_cpm:.2f} per 1k views
    Status: Global Deployment Active
    Goal: Monetization by Feb 2026
    ----------------------------------------------
    """
    with open("revenue_report.txt", "a") as f:
        f.write(report_content)
    print("📈 Revenue Report Updated.")

def apply_alpha_grading(image):
    """AI Teal & Orange: Cinematic Hollywood look."""
    img = image.astype(float)
    img[:, :, 0] *= 1.15  # Warm Oranges
    img[:, :, 2] *= 1.12  # Cold Teals
    return np.clip(img, 0, 255).astype('uint8')

def apply_kasmandra_vfx(image, t):
    """Aggressive screen shake and RGB split on impact."""
    if 2.8 <= t <= 4.2: # Impact window
        shift = random.randint(-45, 45)
        image = np.roll(image, shift, axis=0)
        image[:, :, 0] = np.roll(image[:, :, 0], 20, axis=1)
    return apply_alpha_grading(image)

async def run_engine():
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")

        # 1. SELECT NICHE & TRENDS
        niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
        tags = stalk_trending_hashtags(niche)

        # 2. FETCH 4K CHARACTERS
        headers = {"Authorization": PEXELS_API}
        queries = {'JOHN_WICK': 'hitman combat tactical 4k', 'FAST_FURIOUS': 'supercar drift 4k', 'MARVEL': 'cinematic superhero 4k'}
        res = requests.get(f"https://api.pexels.com/videos/search?query={queries[niche]}&per_page=15&orientation=portrait", headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
        
        with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

        # 3. SPEED RAMPING & VFX
        raw_clip = VideoFileClip("raw.mp4").resized(height=1920).cropped(x_center=540, width=1080)
        c1 = raw_clip.subclipped(0, 2.8).with_effects([vfx.MultiplySpeed(1.8)])
        c2 = raw_clip.subclipped(2.8, 4.2).with_effects([vfx.MultiplySpeed(0.4)]) # SLOW MO
        c3 = raw_clip.subclipped(4.2, 6.0).with_effects([vfx.MultiplySpeed(2.2)])
        clip = concatenate_videoclips([c1, c2, c3])
        
        # Apply VFX (v2.0 MoviePy Fix)
        clip = clip.image_transform(lambda img, t: apply_kasmandra_vfx(img, t))

        # 4. AUDIO & TEXT
        audio = AudioFileClip("audio.mp3").with_duration(clip.duration).with_volume_scaled(3.0)
        txt = TextClip(text=f"{niche}", font_size=180, color='white', font="Arial-Bold", stroke_color="black", stroke_width=12, method='caption', size=(1000, None))
        txt = txt.with_duration(clip.duration).with_position(('center', 'center'))

        # 5. EXPORT & DEPLOY
        final = CompositeVideoClip([clip, txt]).with_audio(audio)
        final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"{niche} 💀 // GTA 6 GRAPHICS {tags}")
        uploaded = channel.upload_video(video)
        
        # 6. ANALYTICS & REVENUE TRACKING
        generate_revenue_report(uploaded.id, niche)
        print(f"🌍 GLOBAL SUCCESS: https://youtu.be/{uploaded.id}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_engine())

