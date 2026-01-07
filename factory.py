import os, requests, random, time, wave, struct, pickle, math
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq

# --- KEY ROTATION ---
# Add your keys to GitHub Secrets: GEMINI_KEY_1, GROQ_KEY
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    """Cycles through Gemini and Groq for Unlimited SEO"""
    topic = random.choice(["Cyberpunk 2026", "Realistic GTA 6", "Marvel CGI", "Demon Samurai"])
    prompt_text = f"Viral SEO: {topic}. Format: Title | Desc | Tags | ImagePrompt"
    
    # Try Gemini
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            client = Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt_text)
            return parse_meta(resp.text)
        except: continue

    # Backup: Groq
    if GROQ_KEY:
        try:
            client = Groq(api_key=GROQ_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt_text}]
            )
            return parse_meta(resp.choices[0].message.content)
        except: pass

    return {"title": f"Epic {topic}", "desc": "CGI", "tags": ["CGI"], "prompt": f"8k {topic}"}

def parse_meta(text):
    p = text.split("|")
    return {"title": p[0].strip(), "desc": p[1].strip(), "tags": p[2].split(","), "prompt": p[3].strip()}

def generate_aggressive_phonk(duration, filename="audio.wav"):
    """Generates Distorted 808 Bass beats"""
    fps = 44100
    with wave.open(filename, 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            pulse = (i % (fps // 2)) < (fps // 8) # 130 BPM Pulse
            if pulse:
                val = math.sin(2 * math.pi * 45 * (i / fps))
                val = max(-0.8, min(0.8, val * 5.0)) # Heavy Distortion
                f.writeframesraw(struct.pack('<h', int(val * 32767)))
            else:
                f.writeframesraw(struct.pack('<h', 0))

def build_video(meta):
    print(f"🎬 Producing: {meta['title']}")
    clips = []
    for i in range(12): # Fast cuts for retention
        seed = random.randint(1, 99999)
        url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={seed}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        
        # Create Epic Shake
        clip = ImageClip(f"f{i}.jpg").set_duration(0.5) # Total ~6 seconds
        def shake(get_frame, t):
            frame = get_frame(t)
            s = 20
            return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
        clips.append(clip.fl(shake))
    
    video = concatenate_videoclips(clips, method="compose")
    generate_aggressive_phonk(video.duration, "audio.wav")
    
    # CRASH FIX: Align audio and video durations exactly
    audio = AudioFileClip("audio.wav")
    # We use audio.duration as the 'truth' to avoid OSError
    final_video = video.set_duration(audio.duration).set_audio(audio)
    
    final_video.write_videofile("upload_ready.mp4", fps=30, codec="libx264", logger=None)
    return "upload_ready.mp4"

def upload_to_youtube(video_file, meta):
    if not os.path.exists('token.json'): return
    with open('token.json', 'rb') as t: credentials = pickle.load(t)
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        'snippet': {'title': meta['title'], 'description': meta['desc'], 'tags': meta['tags'], 'categoryId': '24', 'defaultLanguage': 'en'},
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False},
        'recordingDetails': {'locationDescription': 'USA', 'location': {'latitude': 37.09, 'longitude': -95.71}}
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media).execute()
    print("🚀 Video is live and targeted to USA!")

if __name__ == "__main__":
    m = get_metadata()
    v = build_video(m)
    upload_to_youtube(v, m)

