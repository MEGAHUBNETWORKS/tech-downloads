import os, asyncio, random, math, requests, datetime, pickle, time
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
# --- SUPPRESS WARNINGS ---
warnings.filterwarnings("ignore", category=FutureWarning)
# --- MASTER CONFIG ---
# Replace with your actual Pexels API Key
PEXELS_API = os.getenv('PEXELS_API_KEY') 
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def stalk_trending_hashtags(niche):
    """Targets high-growth tags for global reach."""
    trending_pools = {
        'JOHN_WICK': "#johnwick #sigma #edit #action #4k #revenge #gangster #cinematic",
        'FAST_FURIOUS': "#drift #jdm #supercars #fastandfurious #gta6 #phonk #racing",
        'MARVEL': "#avengers #marvel #mcu #superhero #badass #darkedit #cold #phonk"
    }
    return trending_pools.get(niche, "#viral #shorts #2026")

def apply_alpha_grading(image):
    """AI Teal & Orange: Hollywood standard for high-action characters."""
    img = image.astype(float)
    img[:, :, 0] *= 1.18  # Push Oranges (Skin/Fire)
    img[:, :, 2] *= 1.15  # Push Teals (Steel/Atmosphere)
    return np.clip(img, 0, 255).astype('uint8')

def apply_kasmandra_vfx(image, t, impact_start, impact_end):
    """Aggressive screen shake and RGB split on impact points."""
    if impact_start <= t <= impact_end:
        shift = random.randint(-50, 50)
        image = np.roll(image, shift, axis=0) # Shake
        image[:, :, 0] = np.roll(image[:, :, 0], 25, axis=1) # Chromatic Glitch
    return apply_alpha_grading(image)

async def produce_and_upload():
    try:
        # 1. LOGIN
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")

        # 2. NICHE & TAG SELECTION
        niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
        tags = stalk_trending_hashtags(niche)
        print(f"🎬 Current Production: {niche}")

        # 3. FETCH 4K CHARACTERS (Targeting long, detailed action)
        headers = {"Authorization": PEXELS_API}
        queries = {
            'JOHN_WICK': 'hitman fighting martial arts 4k', 
            'FAST_FURIOUS': 'supercar drift racing 4k', 
            'MARVEL': 'cinematic superhero battle 4k'
        }
        res = requests.get(f"https://api.pexels.com/videos/search?query={queries[niche]}&per_page=15&orientation=portrait&min_duration=8", headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
        
        with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

        # 4. ADAPTIVE SPEED RAMPING (GTA 6 Trailer Style)
        raw_clip = VideoFileClip("raw.mp4").resized(height=1920).cropped(x_center=540, width=1080)
        total_dur = raw_clip.duration
        target_dur = min(total_dur, 8.5)
        mid = target_dur / 2
        
        # Ramp: Fast -> SLOW MO -> Fast
        c1 = raw_clip.subclipped(0, mid - 0.7).with_effects([vfx.MultiplySpeed(1.8)])
        c2 = raw_clip.subclipped(mid - 0.7, mid + 0.8).with_effects([vfx.MultiplySpeed(0.4)]) 
        c3 = raw_clip.subclipped(mid + 0.8, target_dur).with_effects([vfx.MultiplySpeed(2.2)])
        clip = concatenate_videoclips([c1, c2, c3])
        
        # Calculate impact timestamps for the VFX function
        imp_start = (mid - 0.7) / 1.8
        imp_end = imp_start + (1.5 / 0.4)

        # 5. VFX & COLOR GRADING (MoviePy v2.0 Image Transform)
        clip = clip.image_transform(lambda img, t: apply_kasmandra_vfx(img, t, imp_start, imp_end))

        # 6. AUDIO & 4K EXPORT
        # Ensure you have a 'audio.mp3' or link it to a dynamic phonk source
        audio = AudioFileClip("audio.mp3").with_duration(clip.duration).with_volume_scaled(3.5)
        
        txt = TextClip(text=f"{niche} // 2026", font_size=170, color='white', font="Arial-Bold", 
                       stroke_color="black", stroke_width=15, method='caption', size=(1000, None))
        txt = txt.with_duration(clip.duration).with_position(('center', 'center'))

        final = CompositeVideoClip([clip, txt]).with_audio(audio)
        final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

        # 7. DEPLOY
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"{niche} 💀 // REAL LIFE GTA 6 GRAPHICS {tags}")
        video.set_description(f"GET ACCESS: {LINK}")
        uploaded = channel.upload_video(video)
        print(f"🌍 GLOBAL SUCCESS: Video {uploaded.id} is Live.")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

async def main_loop():
    """Human-Randomized Scheduler for 24/7 Operation"""
    while True:
        await produce_and_upload()
        
        # Wait between 3 to 5 hours (180 - 300 minutes)
        wait_time = random.randint(180, 300)
        next_run = datetime.datetime.now() + datetime.timedelta(minutes=wait_time)
        print(f"💤 Sleeping. Next randomized upload at: {next_run.strftime('%H:%M:%S')}")
        await asyncio.sleep(wait_time * 60)

if __name__ == "__main__":
    asyncio.run(main_loop())

