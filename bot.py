import os, asyncio, random, edge_tts, math
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, VideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIGURATION ---
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def make_animation(t):
    """Generates a hypnotic, high-contrast animated frame."""
    surface = np.zeros((1920, 1080, 3), dtype="uint8")
    # Create pulsing circles and geometric patterns
    for i in range(5):
        radius = int(200 + 100 * math.sin(t * 3 + i))
        center = (540 + int(100 * math.cos(t * 2)), 960 + int(100 * math.sin(t * 2)))
        color = (random.randint(0, 50), random.randint(150, 255), 255) # Electric Blue/Cyan
        # Simplified drawing logic for speed
        surface[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius] = color
    return surface

async def run_engine():
    # 1. TOPIC & SEO
    niches = ['DEEP WEB SECRETS', 'GTA 6 GLITCH', 'IPHONE 18 LEAK', 'AI WEALTH HACK']
    topic = random.choice(niches)
    print(f"🔥 Generating Animation for: {topic}")

    # 2. AI SCRIPT & VOICE
    script = f"STOP! You just found the only working {topic} in 2026. 🤫 Everyone is gatekeeping this link, but I'm giving it to you for free. Check the link in my description right now! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+30%").save("voice.mp3")
    voice = AudioFileClip("voice.mp3")
    duration = voice.duration - 0.05

    # 3. GENERATE ANIMATED BACKGROUND
    # This creates a unique 1080x1920 animated background using the math function above
    bg_animation = VideoClip(make_animation, duration=duration).with_fps(30)

    # 4. PRO EDITING
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path): font_path = "Arial"

    # Animated Subtitles (Yellow/Black for high contrast)
    subs = TextClip(text=script, font_size=85, color='yellow', font=font_path, 
                    method='caption', size=(950, None), stroke_color="black", stroke_width=2).with_duration(duration).with_position(('center', 'center'))
    
    # Viral Progress Bar
    bar_bg = ColorClip(size=(1080, 20), color=(20, 20, 20)).with_duration(duration).with_position(('center', 1880))
    bar_moving = ColorClip(size=(1080, 20), color=(0, 255, 127)).with_duration(duration).with_position((0, 1880))
    bar_moving = bar_moving.with_effects([vfx.Resize(lambda t: (max(1, int(1080 * t/duration)), 20))])

    # 5. MASTERING & EXPORT
    final = CompositeVideoClip([bg_animation, subs, bar_bg, bar_moving]).with_audio(voice.subclipped(0, duration))
    final.write_videofile("final.mp4", fps=30, bitrate="10000k", codec="libx264")

    # 6. AUTOMATIC UPLOAD
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"THE {topic} THEY DON'T WANT YOU TO SEE! 🤫 #shorts #viral")
        video.set_description(f"GET THE LINK HERE: {LINK}\n\nThis {topic} is life changing.")
        video.set_privacy_status("public")
        channel.upload_video(video)
        print(f"✅ SUCCESS: {topic} is Live!")
    except Exception as e:
        print(f"❌ UPLOAD FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(run_engine())

