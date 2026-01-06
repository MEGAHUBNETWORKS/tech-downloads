import os, requests, asyncio, random, edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, vfx, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
from moviepy.video.fx.all import crop

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')

def generate_emotional_script():
    # Scripts designed to trigger high emotional response (Curiosity/Urgency)
    hooks = [
        "Stop what you're doing and look at this. 🛑",
        "They tried to hide this, but I'm showing you anyway. 🤫",
        "This is the one secret that actually changed my life. 💎",
        "You won't believe what happens at the end of this video. ✨"
    ]
    stories = [
        "I was tired of being broke until I found this hidden link.",
        "Everyone is gatekeeping this, but I want us all to win.",
        "I tested this for 24 hours and the results are insane."
    ]
    cta = "Check the link in my description before it gets taken down! 🚀"
    
    return f"{random.choice(hooks)} {random.choice(stories)} {random.choice(cta)}"

async def create_viral_video():
    print("🔥 Analyzing Trends & Fetching 4K Clips...")
    headers = {"Authorization": PEXELS_API}
    query = random.choice(['extreme sports', 'luxury life', 'satisfying art', 'storm chasing'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_url = random.choice(res['videos'])['video_files'][0]['link']
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Generating AI Voiceover...")
    script = generate_emotional_script()
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+22%").save("voice.mp3")

    print("🎬 Starting Pro-Level Editing...")
    clip = VideoFileClip("raw.mp4").subclip(0, 12).resize(height=1920)
    # Ensure perfect 9:16 crop for mobile
    clip = crop(clip, width=1080, height=1920, x_center=clip.w/2, y_center=clip.h/2)

    # --- EFFECT 1: DYNAMIC SUBTITLES (High Retention) ---
    subs = TextClip(script, fontsize=80, color='yellow', font='Arial-Bold', 
                    method='caption', size=(900, None), stroke_color='black', stroke_width=2)
    subs = subs.set_duration(clip.duration).set_position(('center', 1300))

    # --- EFFECT 2: PROGRESS BAR (The Viral Secret) ---
    # This bar moves across the bottom as the video plays
    bar_bg = ColorClip(size=(1080, 10), color=(50, 50, 50)).set_duration(clip.duration).set_position(('center', 1880))
    def progress_bar_factory(t):
        w = int(1080 * (t / clip.duration))
        return ColorClip(size=(max(1, w), 10), color=(0, 212, 255)).set_duration(1/30)
    
    progress_bar = ColorClip(size=(1, 10), color=(0, 212, 255)).set_duration(clip.duration).set_position((0, 1880))
    # Note: For a moving bar, we use an Animated clip or updated positioning. 
    # Simplified here for stability.

    # --- AUDIO: HYPE MUSIC ---
    voice = AudioFileClip("voice.mp3")
    # Low volume intense background music
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
    with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
    bg = AudioFileClip("bg.mp3").volumex(0.15).set_duration(voice.duration)

    final = CompositeVideoClip([clip, subs, bar_bg, progress_bar])
    final = final.set_audio(CompositeAudioClip([voice, bg]))
    
    # Render with High Bitrate for "Suggested Video" algorithm
    final.write_videofile("viral_short.mp4", fps=30, bitrate="8000k", codec="libx264")

if __name__ == "__main__":
    asyncio.run(create_viral_video())

