import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_trending_music():
    """Returns a high-energy background track."""
    tracks = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
    ]
    return random.choice(tracks)

async def create_video():
    # 1. Trend Selection
    trending_niches = ['Luxury life', 'Supercars', 'Satisfying tech', 'GTA 6 Gameplay', 'Cyberpunk 2026']
    topic = random.choice(trending_niches)
    print(f"🔥 Step 1: Trending Topic identified: {topic}")
    
    # 2. Fetch Video
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=10&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    # 3. AI Voiceover
    script = f"POV: You found the secret {topic} glitch. 🤫 This is finally working in 2026. Check the link in my description now! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    # 4. Pro Video Editing (v2.0 Fixed Syntax)
    clip = VideoFileClip("raw.mp4")
    
    # DURATION FIX: Sensing the actual video length
    duration = min(clip.duration, 10.0) 
    clip = clip.subclipped(0, duration).resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    
    # Color Boost Fix
    try:
        clip = clip.with_effects([vfx.multiply_color(1.2)])
    except:
        pass

    # Subtitles (FONT FIX: Using DejaVu-Sans which is safe for Linux)
    subs = TextClip(
        text=script, 
        font_size=70, 
        color='yellow', 
        font='DejaVu-Sans-Bold', 
        method='caption', 
        size=(900, None)
    ).with_duration(duration).with_position(('center', 1300))
    
    # Progress Bar Background
    bar_bg = ColorClip(size=(1080, 15), color=(30, 30, 30)).with_duration(duration).with_position(('center', 1880))
    
    # Moving Progress Bar Logic
    def make_bar(t):
        w = int(1080 * (t / duration))
        return ColorClip(size=(max(1, w), 15), color=(0, 212, 255))
    
    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_bar(t).with_position((0, 1880))]))

    # 5. Audio Mastering
    voice = AudioFileClip("voice.mp3")
    music_url = get_trending_music()
    with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
    
    bg_music = AudioFileClip("bg.mp3").with_volume_scaled(0.15).with_duration(duration)
    final_audio = CompositeAudioClip([voice.with_duration(duration), bg_music])

    # 6. Final Composition
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg]).with_audio(final_audio)
    
    print("🚀 Step 4: Finalizing Viral Export...")
    final_video.write_videofile("final.mp4", fps=30, bitrate="8500k", codec="libx264", audio_codec="aac")
    print("✅ SUCCESS: final.mp4 created.")

if __name__ == "__main__":
    asyncio.run(create_video())

