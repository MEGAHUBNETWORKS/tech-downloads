import os, requests, random, time, wave, struct, pickle, math
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq
from PIL import Image, ImageEnhance, ImageFilter

# --- CLOUD CONFIG (GitHub Secrets) ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1"), os.getenv("GEMINI_KEY_2"), os.getenv("GEMINI_KEY_3")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    """Generates Legendary Fight SEO & Prompts"""
    battles = [
        "Goku Ultra Instinct vs Gojo Satoru Infinity",
        "Saitama One Punch Man vs Boros Final Form",
        "Madara Uchiha vs Hashirama Senju Peak",
        "Sukuna vs Mahoraga Shibuya Battle"
    ]
    battle = random.choice(battles)
    # The "Master Prompt" ensures they look real and powerful
    prompt_text = f"Title | Desc | Tags | cinematic anime fight, 8k, hyper-realistic, {battle}, energy auras, lightning sparks, dark atmosphere, destructive environment, high-end CGI movie style"
    
    random.shuffle(GEMINI_KEYS)
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            client = Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_text)
            return parse(resp.text)
        except: continue
    return {"t": f"{battle} Fight", "d": "Epic Battle", "tg": ["anime", "phonk"], "pr": battle}

def parse(t):
    p = t.split("|")
    return {"t": p[0], "d": p[1], "tg": p[2].split(","), "pr": p[3]}

def generate_aggressive_audio(duration):
    """High-energy Phonk with heavy 808 distortion"""
    fps = 44100
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            hit = (i % (fps // 3)) < (fps // 12)
            if hit:
                val = max(-0.9, min(0.9, math.sin(2*math.pi*42*(i/fps))*10)) 
                f.writeframesraw(struct.pack('<h', int(val * 32767)))
            else: f.writeframesraw(struct.pack('<h', 0))

def apply_motion_blur(frame, intensity=5):
    """Creates the 'Tai Lung' speed effect"""
    img = Image.fromarray(frame)
    img = img.filter(ImageFilter.GaussianBlur(radius=intensity))
    return np.array(img)

def build_video(meta):
    clips = []
    for i in range(12): # Fast-cut action
        url = f"https://image.pollinations.ai/prompt/{meta['pr'].replace(' ','%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        with open(f"{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        
        # Grading: Make it Dark & Cinematic
        img = Image.open(f"{i}.jpg")
        img = ImageEnhance.Contrast(img).enhance(1.6)
        img = ImageEnhance.Brightness(img).enhance(0.7)
        img.save(f"{i}.jpg")

        clip = ImageClip(f"{i}.jpg").set_duration(0.4)
        
        def anim(get_frame, t):
            frame = get_frame(t)
            # Zoom-Punch: Screen moves forward fast
            zoom = 1 + (t * 0.3)
            # Add Motion Blur only on the first 0.1s of the hit
            if t < 0.1:
                frame = apply_motion_blur(frame, intensity=8)
            # Random Directional Shake
            s = 30 if t < 0.1 else 5
            return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
            
        clips.append(clip.fl(anim))

    video = concatenate_videoclips(clips, method="compose")
    generate_aggressive_audio(video.duration)
    return video.set_audio(AudioFileClip("audio.wav").set_duration(video.duration))

def upload(file, meta):
    # Same as previous logic using token.json and USA location
    pass

if __name__ == "__main__":
    m = get_metadata()
    v = build_video(m)
    v.write_videofile("out.mp4", fps=30, codec="libx264", logger=None)
    upload("out.mp4", m)
