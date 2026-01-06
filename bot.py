import os, asyncio, random, math, requests, datetime
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def stalk_trending_hashtags(niche):
    trending_pools = {
        'JOHN_WICK': "#johnwick #sigma #edit #action #4k #revenge #gangster",
        'FAST_FURIOUS': "#drift #jdm #supercars #fastandfurious #gta6 #phonk",
        'MARVEL': "#avengers #marvel #mcu #superhero #badass #darkedit #cold"
    }
    return trending_pools.get(niche, "#viral #shorts #2026")

def apply_alpha_grading(image):
    """AI Teal & Orange: Cinematic Hollywood look."""
    img = image.astype(float)
    img[:, :, 0] *= 1.15  # Warm Oranges
    img[:, :, 2] *= 1.12  # Cold Teals
    return np.clip(img, 0, 255).astype('uint8')

def apply_kasmandra_vfx(image, t, impact_start, impact_end):
    """Aggressive screen shake and RGB split on impact."""
    if impact_start <= t <= impact_end:
        shift = random.randint(-45, 45)
        image = np.roll(image, shift, axis=0)
        image[:, :, 0] = np.roll(image[:, :, 0], 20, axis=1)
    return apply_alpha_grading(image)

async def run_engine():
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")

        niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
        tags = stalk_trending_hashtags(niche)

        # 1. FETCH LONGER ASSETS (Targeting 10s+ for more 'Interesting' content)
        headers = {"Authorization": PEXELS_API}
        queries = {'JOHN_WICK': 'hitman fighting martial arts 4k', 'FAST_FURIOUS': 'supercar drift racing 4k', 'MARVEL': 'cinematic superhero battle 4k'}
        res = requests.get(f"https://api.pexels.com/videos/search?query={queries[niche]}&per_page=15&orientation=portrait&min_duration=8", headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
        
        with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

        # 2. ADAPTIVE DURATION LOGIC
        raw_clip = VideoFileClip("raw.mp4").resized(height=1920).cropped(x_center=540, width=1080)
        total_dur = raw_clip.duration
        
        # We target a 7-9 second edit for maximum retention
        target_dur = min(total_dur, 8.5)
        mid = target_dur / 2
        
        # 3. DYNAMIC SPEED RAMPING (Safe from Errors)
        c1 = raw_clip.subclipped(0, mid - 0.7).with_effects([vfx.MultiplySpeed(1.8)])
        c2 = raw_clip.subclipped(mid - 0.7, mid + 0.8).with_effects([vfx.MultiplySpeed(0.4)]) # SLOW MO IMPACT
        c3 = raw_clip.subclipped(mid + 0.8, target_dur).with_effects([vfx.MultiplySpeed(2.2)])
        
        clip = concatenate_videoclips([c1, c2, c3])
        impact_start, impact_end = (mid - 0.7)/1.8, ((mid - 0.7)/1.8) + (1.5/0.4)

        # 4. VFX & COLOR GRADING
        clip = clip.image_transform(lambda img, t: apply_kasmandra_vfx(img, t, impact_start, impact_end))

        # 5. GANGSTER PHONK & OVERLAY
        audio = AudioFileClip("audio.mp3").with_duration(clip.duration).with_volume_scaled(3.0)
        txt = TextClip(text=f"{niche} 💀", font_size=180, color='white', font="Arial-Bold", stroke_color="black", stroke_width=12, method='caption', size=(1000, None))
        txt = txt.with_duration(clip.duration).with_position(('center', 'center'))

        # 6. EXPORT (Elite 30,000k Bitrate)
        final = CompositeVideoClip([clip, txt]).with_audio(audio)
        final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

        # 7. UPLOAD
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"{niche} // 4K GTA 6 GRAPHICS {tags}")
        uploaded = channel.upload_video(video)
        print(f"🌍 GLOBAL SUCCESS: https://youtu.be/{uploaded.id}")

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_engine())

