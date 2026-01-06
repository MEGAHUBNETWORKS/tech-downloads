import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

async def create_video():
    print("🎬 Fetching High-Retention Content...")
    headers = {"Authorization": PEXELS_API}
    query = random.choice(['expensive cars', 'ocean', 'satisfying', 'modern house'])
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Generating AI Script...")
    hooks = ["Wait for the end! 🛑", "This is a glitch! 🤫", "Free hack! 💎"]
    script = f"{random.choice(hooks)} Get your free card at the link in description! 🚀"
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    print("🎨 Rendering (v2.0 Fixed Syntax)...")
    clip = VideoFileClip("raw.mp4").subclipped(0, 10)
    clip = clip.resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    
    # FIX: Using lowercase or multiply_color for v2.0 compatibility
    try:
        clip = clip.with_effects([vfx.multiply_color(1.2)])
    except:
        clip = clip.with_effects([vfx.colorx(1.2)])

    # Subtitles
    subs = TextClip(text=script, font_size=70, color='yellow', method='caption', size=(900, None)).with_duration(clip.duration).with_position(('center', 1300))
    
    # Progress Bar
    bar_bg = ColorClip(size=(1080, 12), color=(40, 40, 40)).with_duration(clip.duration).with_position(('center', 1880))
    def make_bar(t): return ColorClip(size=(max(1, int(1080 * (t/clip.duration))), 12), color=(0, 212, 255))
    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_bar(t).with_position((0, 1880))]))

    voice = AudioFileClip("voice.mp3")
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg]).with_audio(voice)
    final_video.write_videofile("final.mp4", fps=30, bitrate="8000k", codec="libx264")
    
    return tags

def upload_and_pin(tags):
    print("📺 Channel Manager: Finalizing Upload...")
    try:
        channel = Channel()
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        video.set_title(f"DON'T MISS OUT! 🎁 #shorts #{tags[0] if tags else 'viral'}")
        video.set_description(f"CLAIM HERE: {LINK} \n\nTags: {', '.join(tags)}")
        video.set_tags(["shorts", "viral", "2026"] + tags)
        video.set_privacy_status("public")
        
        uploaded = channel.upload_video(video)
        print(f"✅ Video Live: {uploaded.id}")
        
        # --- AUTO COMMENT & PIN ---
        # Note: Pinning requires a slightly more advanced scope, 
        # but the bot can immediately comment.
        # channel.comment_on_video(uploaded.id, f"I just got mine! Click here: {LINK}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    tags = await create_video()
    upload_and_pin(tags)

if __name__ == "__main__":
    asyncio.run(main())

