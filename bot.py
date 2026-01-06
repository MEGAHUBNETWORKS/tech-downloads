import os, asyncio, random, math, requests
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_dynamic_audio():
    """Fetches high-energy tracks from different gangster genres."""
    genres = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # Phonk
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", # Brazilian Funk style
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3" # Aggressive Hardstyle
    ]
    return random.choice(genres)

async def run_engine():
    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")

    # 1. FETCH ULTRA-HIGH DETAIL ASSETS (GTA 6 STYLE)
    niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
    queries = {
        'JOHN_WICK': 'hitman combat tactical fighting 4k',
        'FAST_FURIOUS': 'supercar drift street racing night 4k',
        'MARVEL': 'dark superhero cinematic battle 4k'
    }
    
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={queries[niche]}&per_page=20&orientation=portrait"
    video_data = random.choice(requests.get(url, headers=headers).json()['videos'])
    
    with open("raw.mp4", 'wb') as f:
        f.write(requests.get(video_data['video_files'][0]['link']).content)

    # 2. SPEED RAMPING & SLOW-MO IMPACT
    # This creates the 'Professional' rhythm of fast-fast-SLOW-fast
    clip = VideoFileClip("raw.mp4").resized(height=1920).cropped(x_center=540, width=1080).subclipped(0, 7)
    
    # Apply Speed Ramp: Start fast (1.5x), hit slow-mo (0.5x) at the 3-second mark
    clip_start = clip.subclipped(0, 3).with_effects([vfx.MultiplySpeed(1.5)])
    clip_impact = clip.subclipped(3, 4.5).with_effects([vfx.MultiplySpeed(0.5)]) # SLOW MO IMPACT
    clip_end = clip.subclipped(4.5, 6).with_effects([vfx.MultiplySpeed(1.8)])
    
    from moviepy import concatenate_videoclips
    clip = concatenate_videoclips([clip_start, clip_impact, clip_end])

    # 3. KASMANDRA VISUALS (Flicker, Shake, Chromatic)
    def cinematic_vfx(get_frame, t):
        frame = get_frame(t)
        # Match pulse to the new Speed Ramp rhythm
        is_impact = 3.0 <= t <= 4.5 
        
        if is_impact:
            # Extreme Shake + RGB Split (Chromatic Aberration)
            frame = np.roll(frame, random.randint(-60, 60), axis=0)
            frame[:, :, 0] = np.clip(frame[:, :, 0] * 1.5, 0, 255) # Red Boost
        
        # High-Speed Flicker for the rest of the clip
        elif (t * 8) % 1 > 0.8:
            frame = np.clip(frame.astype(float) * 1.3, 0, 255).astype('uint8')
            
        return frame

    clip = clip.fl(cinematic_vfx)

    # 4. RANDOMIZED GANGSTER AUDIO (Maximum Bass)
    music_url = get_dynamic_audio()
    with open("audio.mp3", "wb") as f:
        f.write(requests.get(music_url).content)
    
    # 3.5x Volume scaling for that "Ear-Rape Phonk" vibe people love in edits
    audio = AudioFileClip("audio.mp3").with_duration(clip.duration).with_volume_scaled(3.5)

    # 5. OVERLAY (Vibrating GTA-Style Text)
    txt = TextClip(text=f"{niche} // ELITE", font_size=180, color='white', font="Arial-Bold", 
                   stroke_color="black", stroke_width=15, method='caption', size=(1000, None))
    txt = txt.with_duration(clip.duration).with_position(('center', 'center'))

    # 6. EXPORT & DEPLOY (30,000k Bitrate for Full Detail)
    final = CompositeVideoClip([clip, txt]).with_audio(audio)
    final.write_videofile("final.mp4", fps=30, bitrate="30000k", codec="libx264")

    video = LocalVideo(file_path="final.mp4")
    video.set_title(f"{niche} EDIT // UNSTOPPABLE 💀 #phonk #gta6 #action #4k")
    uploaded = channel.upload_video(video)
    
    print(f"✅ MILIONS GOAL: Video {uploaded.id} is Live with Dynamic Phonk!")

if __name__ == "__main__":
    asyncio.run(run_engine())

