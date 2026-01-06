import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def generate_viral_script():
    """Generates a high-retention script to trigger curiosity and FOMO."""
    hooks = [
        "Stop scrolling! This secret is about to expire. 🛑",
        "The 1% don't want you to know about this link. 🤫",
        "I found a glitch that actually pays out. Look! 💎",
        "Why is nobody talking about this free method? ✨"
    ]
    stories = [
        "I just used this to grab my hundred dollar card in seconds.",
        "It's finally back online after being down for weeks.",
        "I tested this live and it worked on the first try."
    ]
    cta = f"Click the link in the description before it's gone! 🚀"
    return f"{random.choice(hooks)} {random.choice(stories)} {random.choice(cta)}"

async def create_viral_video():
    print("🎬 Step 1: Fetching Trending 4K Footage...")
    headers = {"Authorization": PEXELS_API}
    query = random.choice(['extreme sports', 'luxury lifestyle', 'abstract satisfying', 'deep sea'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    
    try:
        res = requests.get(url, headers=headers).json()
        video_url = random.choice(res['videos'])['video_files'][0]['link']
    except Exception as e:
        print(f"Error fetching Pexels: {e}")
        return

    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Step 2: Generating AI Voiceover...")
    script = generate_viral_script()
    voice_choice = random.choice(["en-US-GuyNeural", "en-GB-SoniaNeural"])
    await edge_tts.Communicate(script, voice_choice, rate="+25%").save("voice.mp3")

    print("🎨 Step 3: High-End Rendering (FX & Progress Bar)...")
    # Load and Prepare Clip
    clip = VideoFileClip("raw.mp4").subclipped(0, 12)
    
    # Smart Crop for 9:16 Shorts format
    target_aspect = 1080 / 1920
    if (clip.w / clip.h) > target_aspect:
        # Landscape to Portrait
        new_w = clip.h * target_aspect
        clip = clip.cropped(x_center=clip.w/2, width=new_w)
    clip = clip.resized(height=1920)

    # Apply Color Boost for 'Pop' effect
    clip = clip.with_effects([vfx.Colorx(1.2)])

    # Add Subtitles (Middle-Bottom)
    subs = TextClip(
        text=script, 
        font_size=70, 
        color='yellow', 
        font='Arial-Bold', 
        method='caption', 
        size=(900, None)
    ).with_duration(clip.duration).with_position(('center', 1300))

    # Add Progress Bar (Bottom)
    # Background bar
    bar_bg = ColorClip(size=(1080, 12), color=(40, 40, 40)).with_duration(clip.duration).with_position(('center', 1880))
    # Moving progress bar
    def make_progress_bar(t):
        w = int(1080 * (t / clip.duration))
        return ColorClip(size=(max(1, w), 12), color=(0, 212, 255))

    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_progress_bar(t).with_position((0, 1880))]))

    # Audio Setup
    voice_audio = AudioFileClip("voice.mp3")
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
    with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
    bg_music = AudioFileClip("bg.mp3").with_volume_scaled(0.15).with_duration(voice_audio.duration)

    final_audio = CompositeAudioClip([voice_audio, bg_music])
    
    # Final Composition
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg])
    final_video = final_video.with_audio(final_audio)

    print("🚀 Step 4: Finalizing Viral Export...")
    final_video.write_videofile("final.mp4", fps=30, bitrate="8000k", codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    asyncio.run(create_viral_video())

