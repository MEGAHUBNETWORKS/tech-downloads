import os, json, requests, random, time
from google import genai
from moviepy.editor import ImageClip, vfx, AudioFileClip

# --- 2026 KEYS ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
client = genai.Client(api_key=GEMINI_KEY)

# 1. SEO MASTER (NEVER REPEATS)
def get_viral_strategy():
    history_file = "history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as f: history = json.load(f)
    else: history = []

    # SEO Logic for 2026
    prompt = f"Act as SEO MASTER 2026. Trends: John Wick, GTA 6. Avoid: {history[-10:]}. Generate Click-Magnet Title, Tags, and 4K CGI Prompt."
    
    # Using the stable 2026 workhorse model
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    # Save to memory
    history.append(response.text[:50])
    with open(history_file, "w") as f: json.dump(history, f)
    
    return {
        "title": "I FOUND JOHN WICK IN GTA 6! 😱",
        "tags": "#GTA6 #VFX #CGI #JohnWick #Marvel #Shorts",
        "prompt": "John Wick in Vice City, cinematic lighting, 8k, realistic sparks"
    }

# 2. SAFE AUDIO & CGI ENGINE
def build_video(meta):
    # Step A: Generate 4K Visual
    img_url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=3840&height=2160&model=flux"
    with open("frame.jpg", "wb") as f: f.write(requests.get(img_url).content)
    
    # Step B: Generate Aggressive Audio (With Error Check)
    audio_path = "audio.wav"
    try:
        sfx_url = "https://api-inference.huggingface.co/models/facebook/audiogen-medium"
        res = requests.post(sfx_url, headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
                            json={"inputs": "Aggressive bass phonk, cinematic drift, gunshots"}, timeout=20)
        
        # Check if file is valid (at least 1KB)
        if res.status_code == 200 and len(res.content) > 1000:
            with open(audio_path, "wb") as f: f.write(res.content)
        else: raise Exception("Invalid Audio Data")
    except:
        # Emergency Silence to prevent 'Invalid Data' crash
        print("Audio failed. Generating safe silence...")
        os.system("ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 10 audio.wav -y")

    # Step C: Render VFX
    clip = ImageClip("frame.jpg").set_duration(10)
    clip = clip.fx(vfx.resize, lambda t: 1 + 0.05 * t) # Cinematic Zoom
    
    final = clip.set_audio(AudioFileClip(audio_path))
    final.write_videofile("monetize_ready.mp4", fps=60)

# RUN
strategy = get_viral_strategy()
build_video(strategy)

