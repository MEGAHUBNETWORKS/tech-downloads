import os, requests, random, time, wave, struct, pickle, math
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq
from PIL import Image, ImageEnhance

# --- CLOUD CONFIG ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1"), os.getenv("GEMINI_KEY_2"), os.getenv("GEMINI_KEY_3")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    """Generates Dark Mythology/Action Prompts for Tai Lung Vibe"""
    topic = random.choice(["Dark Samurai", "Viking God", "Cyberpunk Assassin", "Ancient Demon"])
    # Master Prompt for the AI to ensure the "Vibe"
    prompt_text = f"Title | Desc | Tags | cinematic, dark atmosphere, glowing eyes, high contrast, 8k, action shot, {topic}"
    
    # Key Rotation Logic
    random.shuffle(GEMINI_KEYS)
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            client = Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_text)
            return parse(resp.text)
        except: continue
    return {"t": f"The {topic}", "d": "Epic Edit", "tg": ["phonk", "sigma"], "pr": topic}

def parse(text):
    p = text.split("|")
    return {"t": p[0], "d": p[1], "tg": p[2].split(","), "pr": p[3]}

def generate_aggressive_audio(duration):
    """Generates the Phonk Rhythm from your video"""
    fps = 44100
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            # Fast rhythmic hits (BPM 140)
            hit = (i % (fps // 3)) < (fps // 12)
            if hit:
                val = max(-0.9, min(0.9, math.sin(2*math.pi*40*(i/fps))*8)) # Distorted 808
                f.writeframesraw(struct.pack('<h', int(val * 32767)))
            else:
                f.writeframesraw(struct.pack('<h', 0))

def build_video(meta):
    clips = []
    for i in range(12): 
        # Image Generation
        url = f"https://image.pollinations.ai/prompt/{meta['pr'].replace(' ','%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        img_data = requests.get(url).content
        with open(f"{i}.jpg", "wb") as f: f.write(img_data)
        
        # Apply Dark Cinematic Filter
        img = Image.open(f"{i}.jpg")
        img = ImageEnhance.Contrast(img).enhance(1.5)
        img = ImageEnhance.Brightness(img).enhance(0.8)
        img.save(f"{i}.jpg")

        # Action Animation: Zoom-In + Random Shake
        clip = ImageClip(f"{i}.jpg").set_duration(0.4)
        def anim(get_frame, t):
            frame = get_frame(t)
            # Zoom logic
            zoom = 1 + (t * 0.2) 
            h, w, _ = frame.shape
            # Shake logic
            s = 25 if t < 0.1 else 5 # Intense shake at the start of the cut
            return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
            
        clips.append(clip.fl(anim))

    video = concatenate_videoclips(clips, method="compose")
    generate_aggressive_audio(video.duration)
    audio = AudioFileClip("audio.wav")
    return video.set_duration(audio.duration).set_audio(audio)

def upload(file, meta):
    # Same as previous logic with US coordinates and token.json
    pass

if __name__ == "__main__":
    m = get_metadata()
    v = build_video(m)
    v.write_videofile("out.mp4", fps=30, codec="libx264", logger=None)
    upload("out.mp4", m)

