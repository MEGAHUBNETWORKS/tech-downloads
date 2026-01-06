import os, asyncio, random, math, requests
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, VideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIG ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def generate_aggressive_frame(t, vibe):
    """Generates 4K-ready, high-speed aggressive visuals with shake logic."""
    # Create base surface
    surface = np.zeros((1920, 1080, 3), dtype="uint8")
    
    # BEAT DETECTION LOGIC (Simulated high-bpm pulse)
    # Flashes every 0.2 seconds to match Phonk BPM
    is_beat = True if (t * 5) % 1 > 0.8 else False
    
    # SCREEN SHAKE OFFSET
    off_x = random.randint(-20, 20) if is_beat else 0
    off_y = random.randint(-20, 20) if is_beat else 0

    if vibe == 'HACKER':
        # Cyber-Grid with Red Alert Flashes
        color = (255, 0, 0) if is_beat else (0, 255, 60)
        for i in range(15):
            x = int(540 + off_x + 450 * math.sin(t * 20 + i))
            if 0 <= x < 1080: surface[:, x-8:x+8] = color
            
    elif vibe == 'SPEED':
        # Kinetic Warp Drive effect
        color = (255, 255, 255) if is_beat else (0, 150, 255)
        for i in range(20):
            radius = int(50 + (t * 2000) % 1000)
            center = (540 + off_x, 960 + off_y)
            # Draw fast expanding circles
            # (Simplified for performance)
            surface[max(0,center[1]-5):min(1919,center[1]+5), :] = color
            
    elif vibe == 'WAR':
        # High-contrast thermal/glitch flicker
        if is_beat:
            surface[:, :] = (255, 255, 255) # Whiteout flash
        else:
            surface[::10, :] = (40, 40, 40) # Scanning lines

    return surface

async def run_engine():
    # 1. SELECT TRENDING VIBE
    vibe = random.choice(['HACKER', 'SPEED', 'WAR'])
    duration = 7.5 # Short duration = higher 'Repeat' rate
    
    # 2. GENERATE HIGH-SPEED VISUALS
    bg = VideoClip(lambda t: generate_aggressive_frame(t, vibe), duration=duration).with_fps(30)

    # 3. SYNC AGGRESSIVE AUDIO
    # Using high-energy Phonk/Hardstyle tracks
    music_urls = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3"
    ]
    res = requests.get(random.choice(music_urls))
    with open("audio.mp3", "wb") as f: f.write(res.content)
    
    audio = AudioFileClip("audio.mp3").with_duration(duration).with_volume_scaled(1.8)

    # 4. OVERLAY GLITCH TEXT
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path): font_path = "Arial"

    labels = {'HACKER': 'ACCESS GRANTED', 'SPEED': 'LIMITLESS', 'WAR': 'EXECUTE'}
    
    txt = TextClip(
        text=labels[vibe], 
        font_size=150, 
        color='white', 
        font=font_path,
        stroke_color="black", 
        stroke_width=5,
        method='caption',
        size=(1000, None)
    ).with_duration(duration).with_position(('center', 'center'))

    # 5. MASTERING
    final = CompositeVideoClip([bg, txt]).with_audio(audio)
    
    # Export with Max Bitrate for 2026 HDR standards
    final.write_videofile("final.mp4", fps=30, bitrate="15000k", codec="libx264")

    # 6. AUTO-UPLOAD
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"{labels[vibe]} // 2026 ⚡ #phonk #edit #aggressive")
        video.set_description(f"GET THE REWARD: {LINK}")
        video.set_privacy_status("public")
        channel.upload_video(video)
        print(f"✅ DEPLOYED: {vibe}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_engine())

