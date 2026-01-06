import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- MASTER CONFIGURATION ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_trending_bg_music():
    """Fetches high-energy viral tracks to keep the algorithm fresh."""
    tracks = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-16.mp3"
    ]
    return random.choice(tracks)

def get_smart_metadata(topic, raw_tags):
    """SEO Logic: Curiosity Gap Titles + High-Rank Tags."""
    hooks = [
        f"THEY HIDE THIS {topic.upper()} SECRET! 🤫",
        f"Working {topic} glitch Jan 2026 💎",
        f"Don't miss these {topic} rewards! 🛑",
        f"POV: You found the {topic} hack 🚀"
    ]
    title = f"{random.choice(hooks)} #shorts #viral #trending"
    description = (
        f"Claim your rewards here: {LINK}\n\n"
        f"Discovering the best of {topic} in 2026. "
        f"Tags: {', '.join(raw_tags)}"
    )
    return title, description

async def run_engine():
    # 1. ANALYZE & FETCH TRENDING VISUALS
    niches = ['Luxury technology', 'GTA 6 leak', 'Supercar secrets', 'Satisfying automation']
    topic = random.choice(niches)
    print(f"🔥 Analyzing Trend: {topic}")

    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=15&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    raw_tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: 
        f.write(requests.get(video_data['video_files'][0]['link']).content)

    # 2. AI SCRIPT & VOICE GENERATION
    script = f"Wait! This {topic} secret is blowing up right now. Check the link in my description to get the rewards before they patch it. It works in 2026! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+28%").save("voice.mp3")

    # 3. PRO VIDEO EDITING (v2.0 UNBREAKABLE)
    voice = AudioFileClip("voice.mp3")
    final_duration = voice.duration - 0.05 # Safety buffer to prevent OSError
    
    # FETCH MUSIC
    try:
        music_url = get_trending_bg_music()
        with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
        bg_music = AudioFileClip("bg.mp3").with_volume_scaled(0.12).with_duration(final_duration)
    except:
        bg_music = None

    # Process Clip
    clip = VideoFileClip("raw.mp4")
    clip = clip.resized(height=1920).cropped(x_center=clip.w/2, width=1080).subclipped(0, final_duration)
    
    # Linux Font Safety
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    if not os.path.exists(font_path): font_path = "Arial"

    # Subtitles
    subs = TextClip(text=script, font_size=75, color='yellow', font=font_path, 
                    method='caption', size=(900, None)).with_duration(final_duration).with_position(('center', 1300))
    
    # Viral Progress Bar Logic
    bar_bg = ColorClip(size=(1080, 15), color=(30, 30, 30)).with_duration(final_duration).with_position(('center', 1880))
    bar_moving = ColorClip(size=(1080, 15), color=(0, 212, 255)).with_duration(final_duration).with_position((0, 1880))
    bar_moving = bar_moving.with_effects([vfx.Resize(lambda t: (max(1, int(1080 * t/final_duration)), 15))])

    # Audio Mastering
    audio_list = [voice.subclipped(0, final_duration)]
    if bg_music: audio_list.append(bg_music)
    final_audio = CompositeAudioClip(audio_list)
    
    # Build Final
    final = CompositeVideoClip([clip, subs, bar_bg, bar_moving]).with_audio(final_audio)
    final.write_videofile("final.mp4", fps=30, bitrate="8500k", codec="libx264", audio_codec="aac")

    # 4. AUTOMATIC CHANNEL UPLOAD
    try:
        title, desc = get_smart_metadata(topic, raw_tags)
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(title)
        video.set_description(desc)
        video.set_tags(["viral", "shorts", "2026", "money"] + raw_tags)
        video.set_privacy_status("public")
        
        uploaded = channel.upload_video(video)
        print(f"✅ SUCCESS: {title} | ID: {uploaded.id}")
    except Exception as e:
        print(f"❌ UPLOAD FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(run_engine())

