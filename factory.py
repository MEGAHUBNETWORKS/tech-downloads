import os, json, requests, random
from google import genai
from moviepy.editor import ImageClip, vfx, AudioFileClip

# --- 2026 KEY SYNC ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
client = genai.Client(api_key=GEMINI_KEY)

def get_viral_strategy():
    if os.path.exists("history.json"):
        with open("history.json", "r") as f: history = json.load(f)
    else: history = []

    # SEO Master Strategy 2026
    instruction = (
        f"Act as SEO MASTER 2026. Analyze trends for GTA 6 and Marvel. "
        f"Avoid: {history[-10:]}. Generate: 1. Click-Magnet Title, "
        "2. 20 Viral Tags, 3. 4K CGI Prompt."
    )
    
    # 2026 STABLE MODELS:
    # Use 'gemini-2.5-flash' for stability 
    # Use 'gemini-3-flash' for advanced reasoning (if your account has access)
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=instruction
        )
    except Exception as e:
        print(f"Primary model failed, trying fallback: {e}")
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=instruction
        )
    
    history.append(response.text[:50])
    with open("history.json", "w") as f: json.dump(history, f)
    
    # ... rest of your parsing logic

    
    return {
        "title": "I FOUND JOHN WICK IN GTA 6! 😱 (Ultra 4K VFX)",
        "tags": "#GTA6 #JohnWick #Marvel #CGI #VFX #4K #Sigma #Aggressive",
        "prompt": "Cinematic John Wick action, Marvel sparks VFX, GTA 6 ray-tracing, 8k textures"
    }

# --- RENDER ENGINE ---
def build_video(meta):
    # CGI Frame
    url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=3840&height=2160&model=flux"
    with open("frame.jpg", "wb") as f: f.write(requests.get(url).content)
    
    # VFX (Zoom & Slow-Mo)
    clip = ImageClip("frame.jpg").set_duration(10)
    p1 = clip.subclip(0, 5).fx(vfx.resize, lambda t: 1 + 0.05 * t)
    
    # Aggressive AudioGen (Creating the sound now)
    audio_api = "https://api-inference.huggingface.co/models/facebook/audiogen-medium"
    audio_data = requests.post(audio_api, headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
                               json={"inputs": "Aggressive bass phonk, loud gunshot, cinematic drift"}).content
    with open("audio.wav", "wb") as f: f.write(audio_data)
    
    final = p1.set_audio(AudioFileClip("audio.wav"))
    final.write_videofile("monetize_ready.mp4", fps=60)

# RUN FACTORY
meta = get_viral_strategy()
build_video(meta)

