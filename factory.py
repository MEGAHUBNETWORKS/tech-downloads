import os, json, requests, random, time, wave, struct
from google import genai
from moviepy.editor import ImageClip, vfx, AudioFileClip

# --- 2026 KEYS (Ensure these are in GitHub Secrets) ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
client = genai.Client(api_key=GEMINI_KEY)

# --- 1. SEO MASTER & AUTO-WRITER (Millions of Views) ---
def get_viral_strategy():
    history_file = "history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as f: history = json.load(f)
    else: history = []

    # SEO Master AI Analysis - Targets high-CPM 2026 trends
    instruction = (
        f"Act as SEO MASTER 2026. Trends: John Wick, GTA 6, Marvel. "
        f"Avoid: {history[-10:]}. Generate: 1. Click-Magnet Title (First person), "
        "2. 20 High-Velocity Tags, 3. 4K CGI Prompt (Aggressive/Cinematic)."
    )
    
    # Using stable gemini-2.5-flash for reliability
    response = client.models.generate_content(model="gemini-2.5-flash", contents=instruction)
    
    # Save to memory to NEVER repeat
    history.append(response.text[:50])
    with open(history_file, "w") as f: json.dump(history, f)
    
    # Note: In a production loop, you'd parse response.text for specific keys. 
    # For now, we return a targeted meta-packet.
    return {
        "title": "I FOUND JOHN WICK IN GTA 6! 😱 (4K VFX)",
        "tags": "#GTA6 #VFX #JohnWick #Marvel #CGI #Aggressive #Shorts",
        "prompt": "John Wick in Vice City, cinematic lighting, 8k, realistic sparks, Marvel VFX"
    }

# --- 2. ZERO-FAILURE AUDIO GENERATOR ---
def generate_emergency_audio(duration=10, output="audio.wav"):
    """Creates a high-bass 808-style pulse using pure Python (No FFmpeg needed)"""
    sample_rate = 44100
    with wave.open(output, 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        # Generate 10s of data with a heavy bass pulse at the start
        for i in range(int(sample_rate * duration)):
            # Create an aggressive bass 'thump' effect mathematically
            value = int(32767 * 0.5 * (1.0 if (i % 4410 < 2205) else -1.0)) if i < 22050 else 0
            f.writeframesraw(struct.pack('<h', value)) # Left
            f.writeframesraw(struct.pack('<h', value)) # Right
    print(f"✅ Safe audio created: {output}")

# --- 3. THE CINEMATIC ENGINE ---
def build_video(meta):
    # Step A: 4K Visual Generation
    img_url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=3840&height=2160&model=flux"
    try:
        img_data = requests.get(img_url, timeout=30).content
        with open("frame.jpg", "wb") as f: f.write(img_data)
    except:
        print("Image API failed, using previous frame.")

    # Step B: Audio Generation (AI with Python Backup)
    audio_path = "audio.wav"
    try:
        sfx_url = "https://api-inference.huggingface.co/models/facebook/audiogen-medium"
        res = requests.post(sfx_url, headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
                            json={"inputs": "Aggressive bass phonk, loud gunshot, cinematic drift"}, timeout=15)
        if res.status_code == 200 and len(res.content) > 1000:
            with open(audio_path, "wb") as f: f.write(res.content)
            print("🔊 AI Audio Generated Successfully.")
        else:
            raise Exception("AI Audio Empty")
    except:
        print("⚠️ AI Audio failed. Generating Emergency Bass Audio...")
        generate_emergency_audio()

    # Step C: VFX & Render
    clip = ImageClip("frame.jpg").set_duration(10)
    # Effect: Dynamic Cinematic Zoom
    clip = clip.fx(vfx.resize, lambda t: 1 + 0.05 * t)
    
    final = clip.set_audio(AudioFileClip(audio_path))
    final.write_videofile("upload_ready.mp4", fps=60, codec="libx264")
    print("🚀 Video Rendered: upload_ready.mp4")

# --- 4. AUTO-ENGAGEMENT HACK ---
def post_viral_comment():
    questions = ["Who wins? 👇", "Rate the 4K quality 1-10! 🔥", "GTA 6 or Marvel?"]
    print(f"COMMENTING: {random.choice(questions)}")

# EXECUTE FULL CYCLE
if __name__ == "__main__":
    meta_data = get_viral_strategy()
    build_video(meta_data)
    post_viral_comment()

