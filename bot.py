import os, requests, asyncio, random, edge_tts
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# --- SETTINGS ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def generate_viral_script():
    hooks = ["Stop scrolling! 🛑", "The 1% hide this... 🤫", "Found a glitch! 💎", "Why is nobody talking about this? ✨"]
    stories = ["I grabbed my gift card in seconds.", "It's back online after weeks.", "I tested this live and it worked."]
    cta = f"Link in description! 🚀"
    return f"{random.choice(hooks)} {random.choice(stories)} {random.choice(cta)}"

async def create_video():
    print("🎬 Fetching Content...")
    headers = {"Authorization": PEXELS_API}
    q_list = ['luxury', 'satisfying', 'gaming', 'nature']
    query = random.choice(q_list)
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=portrait"
    
    res = requests.get(url, headers=headers).json()
    video_data = random.choice(res['videos'])
    video_url = video_data['video_files'][0]['link']
    
    # Extract tags from Pexels for SEO
    pexels_tags = [tag['name'] for tag in video_data.get('tags', [])[:5]]
    
    with open("raw.mp4", 'wb') as f: f.write(requests.get(video_url).content)

    print("🎙️ Generating Voiceover...")
    script = generate_viral_script()
    await edge_tts.Communicate(script, "en-US-GuyNeural", rate="+25%").save("voice.mp3")

    print("🎨 Rendering with Effects...")
    clip = VideoFileClip("raw.mp4").subclipped(0, 12)
    clip = clip.resized(height=1920).cropped(x_center=clip.w/2, width=1080)
    clip = clip.with_effects([vfx.Colorx(1.2)])

    subs = TextClip(text=script, font_size=70, color='yellow', method='caption', size=(900, None)).with_duration(clip.duration).with_position(('center', 1300))
    
    # Progress Bar Logic
    bar_bg = ColorClip(size=(1080, 12), color=(40, 40, 40)).with_duration(clip.duration).with_position(('center', 1880))
    def make_bar(t): return ColorClip(size=(max(1, int(1080 * (t/clip.duration))), 12), color=(0, 212, 255))
    progress_bar = clip.fl(lambda gf, t: CompositeVideoClip([gf(t), make_bar(t).with_position((0, 1880))]))

    voice = AudioFileClip("voice.mp3")
    final_video = CompositeVideoClip([progress_bar, subs, bar_bg]).with_audio(voice)
    final_video.write_videofile("final.mp4", fps=30, bitrate="8000k", codec="libx264")
    
    return pexels_tags

def upload_to_youtube(video_tags):
    print("📺 Bot Manager: Uploading & Setting SEO...")
    try:
        channel = Channel()
        # Ensure client_secrets.json and credentials.storage are in your GitHub repo
        channel.login("client_secrets.json", "credentials.storage")
        
        video = LocalVideo(file_path="final.mp4")
        
        # SEO Optimization
        video.set_title(f"WAIT FOR IT... 😱 #shorts #{video_tags[0] if video_tags else 'viral'}")
        video.set_description(f"Get it here: {LINK} \n\nRelated: {', '.join(video_tags)}")
        video.set_tags(["shorts", "viral", "money", "2026"] + video_tags)
        video.set_category("Entertainment")
        video.set_default_language("en")
        video.set_embeddable(True)
        video.set_privacy_status("public") # Set to "public" for instant views
        
        # Location Setting (Optional - Set to Global or Specific)
        # video.set_location(latitude=34.0522, longitude=-118.2437) # Example: LA

        uploaded_video = channel.upload_video(video)
        print(f"✅ Success! Video ID: {uploaded_video.id}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

async def main():
    tags = await create_video()
    upload_to_youtube(tags)

if __name__ == "__main__":
    asyncio.run(main())
        
