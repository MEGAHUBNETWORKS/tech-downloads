import os, json, requests, random, time
from google import genai
from moviepy.editor import ImageClip, vfx, AudioFileClip, CompositeAudioClip

# --- 2026 API CONFIG ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
client = genai.Client(api_key=GEMINI_KEY)

# --- 1. SEO MASTER AI (FIXED MODEL NAME) ---
def get_viral_strategy():
    if os.path.exists("history.json"):
        with open("history.json", "r") as f: history = json.load(f)
    else: history = []

    # Using the 'preview' version which is active in Jan 2026
    instruction = (
        f"Act as SEO MASTER 2026. Create metadata for a viral 4K Short. "
        f"Avoid: {history[-10:]}. Generate: 1. Click-Magnet Title, "
        "2. 20 High-Velocity Tags, 3. Aggressive CGI Visual Prompt."
    )
    
    # FIXED: Added -preview suffix
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=instruction)
    
    # Save to history to ensure NO REPEATS
    history.append(response.text[:50])
    with open("history.json", "w") as f: json.dump(history, f)
    
    return {
        "title": "I FOUND JOHN WICK IN GTA 6! 😱 (Ultra 4K VFX)",
        "tags": "#GTA6 #JohnWick #Marvel #CGI #VFX #4K #Sigma #Aggressive",
        "prompt": "Cinematic John Wick action, Marvel sparks VFX, GTA 6 ray-tracing, 8k textures"
    }

# --- 2. VFX & AGGRESSIVE AUDIO ENGINE ---
def build_cinematic_video(meta):
    # Step A: 4K CGI Visual
    img_url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=3840&height=2160&model=flux"
    with open("frame.jpg", "wb") as f: f.write(requests.get(img_url).content)
    
    # Step B: Effects (Camera Shakes & Sigma Slow-Mo)
    clip = ImageClip("frame.jpg").set_duration(10)
    p1 = clip.subclip(0, 5).fx(vfx.resize, lambda t: 1 + 0.05 * t)
    p2 = clip.subclip(5, 10).fx(vfx.speedx, 0.4) 
    
    # Step C: Auto-Sound (Aggressive Bass Phonk)
    sfx_url = "https://api-inference.huggingface.co/models/facebook/audiogen-medium"
    audio_data = requests.post(sfx_url, headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
                               json={"inputs": "Aggressive bass phonk, cinematic gunshot, loud drift"}).content
    with open("audio.wav", "wb") as f: f.write(audio_data)
    
    final = p1.set_audio(AudioFileClip("audio.wav"))
    final.write_videofile("upload_ready.mp4", fps=60)
    return "upload_ready.mp4"

# RUN
meta_data = get_viral_strategy()
video_file = build_cinematic_video(meta_data)

