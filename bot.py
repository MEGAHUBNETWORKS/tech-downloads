import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_viral_seo(topic, tags):
    """Creates high-growth metadata."""
    titles = [f"THEY HIDE THIS {topic} SECRET! 🤫", f"Working {topic} glitch 2026 💎", f"Don't miss this {topic} rewards! 🛑"]
    title = f"{random.choice(titles)} #shorts #viral"
    description = f"Claim rewards here: {LINK}\n\nRelated to: {', '.join(tags)}"
    return title, description

async def create_and_upload():
    # 1. TREND RESEARCH
    topic = random.choice(['Luxury lifestyle', 'Supercars', 'Satisfying tech', 'GTA 6'])
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=10&orientation=portrait"
    
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_data['video_files'][0]['link']).content)

    # 2. AI VOICE & SCRIPT
    script = f"Wait! This {topic} secret is finally back in 2026. Check the link in my description now! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    # 3. PRO EDITING (STABLE v2.0)
    clip = VideoFileClip("raw.mp4")
    duration = min(clip.duration, 10.0) 
    clip = clip.resized(height=1920).cropped(x_center=clip.w/2, width=1080).subclipped(0, duration)
    
    # Font Fix
    font_p = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_p): font_p = "Arial"

    subs = TextClip(text=script, font_size=70, color='yellow', font=font_p, method='caption', size=(900, None)).with_duration(duration).with_position(('center', 1300))
    
    # Progress Bar (Fixed width error)
    bar_bg = ColorClip(size=(1080, 15), color=(30, 30, 30)).with_duration(duration).with_position(('center', 1880))
    # Simple stable bar for v2.0
    bar_moving = ColorClip(size=(1080, 15), color=(0, 212, 255)).with_duration(duration).with_position((0, 1880))
    bar_moving = bar_moving.with_effects([vfx.Resize(lambda t: (max(1, int(1080 * t/duration)), 15))])

    voice = AudioFileClip("voice.mp3")
    final_video = CompositeVideoClip([clip, subs, bar_bg, bar_moving]).with_audio(voice.with_duration(duration))
    final_video.write_videofile("final.mp4", fps=30, bitrate="8000k", codec="libx264")

    # 4. AUTOMATIC UPLOAD
    print("📺 Channel Manager: Uploading to YouTube...")
    try:
        title, desc = get_viral_seo(topic, tags)
        channel = Channel()
        # Ensure client_secrets.json and credentials.storage are in your GitHub repo
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(title)
        video.set_description(desc)
        video.set_tags(["shorts", "viral", "2026"] + tags)
        video.set_privacy_status("public")
        
        channel.upload_video(video)
        print(f"✅ UPLOAD SUCCESSFUL: {title}")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")

if __name__ == "__main__":
    asyncio.run(create_and_upload())

