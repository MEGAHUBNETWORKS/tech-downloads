import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx

# --- SEO & ANALYZER SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def generate_seo_metadata(topic, tags):
    """Creates the Title and Description that forces growth."""
    # List of titles that 'beat' previous performance by increasing curiosity
    viral_titles = [
        f"This {topic} secret is INSANE! 😱 #shorts",
        f"The 1% don't want you knowing this {topic} glitch... 🤫",
        f"I tested this {topic} hack so you don't have to! 💎",
        f"URGENT: Get your {topic} rewards now! 🛑"
    ]
    
    title = random.choice(viral_titles)
    
    # Description optimized for the 2026 'Discovery' algorithm
    description = (
        f"{title}\n\n"
        f"✅ CLAIM YOUR REWARD HERE: {LINK}\n\n"
        f"This is the most viral {topic} video of 2026. "
        "We analyze the trends so you stay ahead. "
        "Follow for more daily glitches!\n\n"
        f"SEO Tags: {', '.join(tags)}, viral, shorts, money, hack"
    )
    
    return title, description

async def create_video():
    trending_niches = ['Luxury life', 'Supercars', 'Satisfying tech', 'GTA 6 Gameplay']
    topic = random.choice(trending_niches)
    
    # FETCH VIDEO & DATA
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=10&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    # Get tags from Pexels to learn what is trending
    raw_tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    # VOICEOVER & EDITING
    script = f"Everyone is looking for {topic}, but they missed the secret link. 🤫 Check my description for the hundred dollar gift card glitch. It works in 2026! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    clip = VideoFileClip("raw.mp4")
    duration = min(clip.duration, 10.0) 
    clip = clip.subclipped(0, duration).resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    
    # FONT PATH (Unbreakable Fix)
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path): font_path = "Arial"

    subs = TextClip(text=script, font_size=70, color='yellow', font=font_path, method='caption', size=(900, None)).with_duration(duration).with_position(('center', 1300))
    
    bar_bg = ColorClip(size=(1080, 15), color=(30, 30, 30)).with_duration(duration).with_position(('center', 1880))
    def make_bar(t): return ColorClip(size=(max(1, int(1080 * (t/duration))), 15), color=(0, 212, 255))
    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_bar(t).with_position((0, 1880))]))

    voice = AudioFileClip("voice.mp3")
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg]).with_audio(voice.with_duration(duration))
    final_video.write_videofile("final.mp4", fps=30, bitrate="8500k", codec="libx264")

    # Generate SEO for the upload
    title, desc = generate_seo_metadata(topic, raw_tags)
    
    # This print helps you see the SEO result in your GitHub logs!
    print(f"✅ VIDEO READY!\nTITLE: {title}\nDESCRIPTION: {desc}")
    return title, desc

if __name__ == "__main__":
    asyncio.run(create_video())
