import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def get_trending_music():
    """Returns a URL for a trending high-energy background track."""
    # These are placeholder URLs for high-retention viral styles
    tracks = [
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # Phonk style
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", # Fast Lo-fi
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3", # Cinematic Tension
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3"  # Aggressive Bass
    ]
    return random.choice(tracks)

async def create_video():
    # 1. Trend Selection
    trending_niches = ['GTA 6 leak', 'iPhone 17 Pro', 'Luxury lifestyle', 'Satisfying tech', 'MrBeast secrets']
    topic = random.choice(trending_niches)
    print(f"🔥 Trending Topic: {topic}")
    
    # 2. Fetch Video
    headers = {"Authorization": PEXELS_API}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page=10&orientation=portrait"
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    tags = [tag['name'].replace(" ", "") for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    # 3. AI Script & Voice
    script = f"POV: You found the only working {topic} link in 2026. 🤫 Everyone is gatekeeping this, but I'm showing you. Check the link in my description now! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+28%").save("voice.mp3")

    # 4. Pro Video Editing
    clip = VideoFileClip("raw.mp4")
    duration = min(clip.duration, 10.0) 
    clip = clip.subclipped(0, duration).resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    
    # Visual Effects (Color Pop)
    try: clip = clip.with_effects([vfx.multiply_color(1.2)])
    except: pass

    # Viral Subtitles
    subs = TextClip(text=script, font_size=75, color='yellow', font='Arial-Bold', 
                    method='caption', size=(920, None), stroke_color="black", stroke_width=2).with_duration(duration).with_position(('center', 1250))
    
    # Animated Progress Bar
    bar_bg = ColorClip(size=(1080, 15), color=(20, 20, 20)).with_duration(duration).with_position(('center', 1880))
    def make_bar(t): return ColorClip(size=(max(1, int(1080 * (t/duration))), 15), color=(0, 212, 255))
    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_bar(t).with_position((0, 1880))]))

    # 5. Trending Audio Sync
    voice = AudioFileClip("voice.mp3")
    music_url = get_trending_music()
    with open("bg.mp3", 'wb') as f: f.write(requests.get(music_url).content)
    
    # Leveling: Voice (100%) + Trending Music (18% volume)
    bg_music = AudioFileClip("bg.mp3").with_volume_scaled(0.18).with_duration(duration)
    final_audio = CompositeAudioClip([voice.with_duration(duration), bg_music])

    # 6. Final Export
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg]).with_audio(final_audio)
    final_video.write_videofile("final.mp4", fps=30, bitrate="9000k", codec="libx264")
    
    return topic, tags

def upload_to_youtube(topic, tags):
    print("📺 Bot Manager: Executing Viral Upload...")
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"THEY DON'T WANT YOU TO KNOW... 🤫 #{topic.replace(' ', '')} #shorts")
        video.set_description(f"GET IT HERE: {LINK}\n\nThis {topic} secret is blowing up! Claim yours before it's gone.")
        video.set_tags(["2026", "viral", "shorts", "money"] + tags)
        video.set_privacy_status("public")
        
        uploaded = channel.upload_video(video)
        print(f"🚀 VIDEO IS LIVE: {uploaded.id}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    topic, tags = await create_video()
    upload_to_youtube(topic, tags)

if __name__ == "__main__":
    asyncio.run(main())

