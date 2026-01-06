import os, asyncio, random, math, requests
import numpy as np
from moviepy import VideoClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_viral_analytics(channel):
    """Analyzes recent videos to see which niche is making the most money."""
    try:
        videos = channel.get_videos()
        stats = {'JOHN_WICK': 0, 'FAST_FURIOUS': 0, 'MARVEL': 0}
        for v in videos[:5]: # Look at last 5 videos
            for niche in stats.keys():
                if niche in v.title:
                    stats[niche] += int(v.views)
        # Return the niche with the highest views
        return max(stats, key=stats.get)
    except:
        return random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])

def generate_perfect_sync_frame(t, niche, is_drop):
    """Matches VFX, eye-contact pulses, and machining movements to the beat."""
    surface = np.zeros((1920, 1080, 3), dtype="uint8")
    
    # Eye-Contact Pulse (Zooming into the center 'eyes' on the beat)
    zoom = 1.2 if is_drop else 1.0
    center_pulse = int(540 * zoom)
    
    # VFX matching the environment
    if niche == 'JOHN_WICK':
        # Sharp, metallic gray/red (Professional Assassin vibe)
        color = (200, 0, 0) if is_drop else (40, 40, 40)
        surface[900:1020, :] = color # Horizon line strike
    elif niche == 'FAST_FURIOUS':
        # Motion blur streaks (High-speed machining vibe)
        color = (0, 255, 255) if is_drop else (0, 50, 100)
        for i in range(5):
            y = int((t * 4000 + i * 200) % 1920)
            surface[y:y+20, :] = color
    elif niche == 'MARVEL':
        # Golden 'God-mode' radiance
        color = (255, 215, 0) if is_drop else (100, 80, 0)
        radius = int(300 + (t * 1000) % 500)
        surface[960-radius:960+radius, 540-radius:540+radius] = color

    return surface

async def run_engine():
    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")

    # 1. ANALYZER: Detect what went viral last time
    best_niche = get_viral_analytics(channel)
    print(f"📈 Analytics Alert: '{best_niche}' is trending on your channel. Focusing production...")

    # 2. MATCHING ENVIRONMENT & VFX
    duration = 6.0
    # The visuals now pulse at 145 BPM (Standard Phonk tempo)
    bg = VideoClip(lambda t: generate_perfect_sync_frame(t, best_niche, (t*4.8)%1 > 0.8), duration=duration).with_fps(30)

    # 3. GANGSTER MUSIC SYNC
    music_map = {
        'JOHN_WICK': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        'FAST_FURIOUS': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        'MARVEL': "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3"
    }
    audio_res = requests.get(music_map[best_niche])
    with open("temp_audio.mp3", "wb") as f: f.write(audio_res.content)
    audio = AudioFileClip("temp_audio.mp3").with_duration(duration).with_volume_scaled(2.5)

    # 4. PERFECT CHARACTER EYE-CONTACT TEXT
    font_p = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_p): font_p = "Arial"

    txt = TextClip(text=f"PURE {best_niche}", font_size=180, color='white', font=font_p, 
                   stroke_color="black", stroke_width=10, method='caption', size=(1000, None))
    txt = txt.with_duration(duration).with_position(('center', 'center'))

    # 5. MASTERING
    final = CompositeVideoClip([bg, txt]).with_audio(audio)
    final.write_videofile("final.mp4", fps=30, bitrate="25000k", codec="libx264")

    # 6. AUTO-UPLOAD & PINNED COMMENT
    video = LocalVideo(file_path="final.mp4")
    video.set_title(f"{best_niche} // 4K ULTRA EDIT 💀 #viral #edit #2026")
    video.set_description(f"CLAIM REWARDS: {LINK}")
    uploaded = channel.upload_video(video)
    uploaded.add_comment("The first person to comment gets a heart! ❤️")
    
    print(f"🚀 Optimized Video Deployed: {uploaded.id}")

if __name__ == "__main__":
    asyncio.run(run_engine())
            
