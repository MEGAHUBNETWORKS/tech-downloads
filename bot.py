import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def generate_seo_metadata(topic, tags):
    viral_titles = [
        f"This {topic} secret is INSANE! 😱 #shorts",
        f"The 1% hide this {topic} glitch... 🤫",
        f"I tested this {topic} hack! 💎",
        f"URGENT: Get your {topic} rewards! 🛑"
    ]
    title = random.choice(viral_titles)
    description = f"{title}\n\n✅ CLAIM HERE: {LINK}\n\nSEO: {', '.join(tags)}"
    return title, description

async def create_video():
    topic = random.choice(['Luxury life', 'Supercars', 'Satisfying tech', 'GTA 6 Gameplay'])
    
    # 1. FETCH VIDEO
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=10&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    raw_tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    # 2. AI VOICE
    script = f"Everyone is looking for {topic}, but they missed the secret link. 🤫 Check my description for the hundred dollar gift card glitch. It works in 2026! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    # 3. EDITING (v2.0 FIXED)
    clip = VideoFileClip("raw.mp4")
    duration = min(clip.duration, 10.0) 
    clip = clip.subclipped(0, duration).resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    
    # Font Logic
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path): font_path = "Arial"

    subs = TextClip(text=script, font_size=70, color='yellow', font=font_path, method='caption', size=(900, None)).with_duration(duration).with_position(('center', 1300))
    
    # PROGRESS BAR FIX (v2.0 Syntax)
    # We create the bar as a separate clip and use a function to update its size over time
    bar_bg = ColorClip(size=(1080, 15), color=(30, 30, 30)).with_duration(duration).with_position(('center', 1880))
    
    def make_progress_bar(t):
        progress_w = max(1, int(1080 * (t / duration)))
        return ColorClip(size=(progress_w, 15), color=(0, 212, 255)).with_duration(1/30)

    # In v2.0, we use CompositeVideoClip to overlay the moving bar
    # We generate the progress bar as a series of frames or a dynamic clip
    progress_bar = ColorClip(size=(1, 15), color=(0, 212, 255)).with_duration(duration).with_position((0, 1880))
    # This effect stretches the bar from width 1 to 1080 over the duration
    progress_bar = progress_bar.with_effects([vfx.Resize(lambda t: (int(1080 * t/duration), 15))])

    voice = AudioFileClip("voice.mp3")
    final_video = CompositeVideoClip([clip, subs, bar_bg, progress_bar]).with_audio(voice.with_duration(duration))
    
    final_video.write_videofile("final.mp4", fps=30, bitrate="8500k", codec="libx264")

    title, desc = generate_seo_metadata(topic, raw_tags)
    print(f"✅ READY: {title}")
    return title, desc

if __name__ == "__main__":
    asyncio.run(create_video())

