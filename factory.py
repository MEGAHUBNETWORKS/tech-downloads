import os, requests, random, time, wave, struct, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq

# --- KEY ROTATION ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    """Cycles through keys for Unlimited SEO"""
    topic = random.choice(["Cyberpunk 2026", "Realistic GTA 6", "Marvel CGI", "Mythology"])
    
    # 1. Try Gemini first
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            client = Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=f"Viral SEO: {topic}. Format: Title | Desc | Tags | Prompt")
            return parse_meta(resp.text)
        except: continue

    # 2. Try Groq (Unlimited Lifetime Backup)
    if GROQ_KEY:
        try:
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Viral SEO: {topic}. Format: Title | Desc | Tags | Prompt"}]
            )
            return parse_meta(completion.choices[0].message.content)
        except Exception as e:
            print(f"Groq error: {e}")

    return {"title": "Epic Scene 2026", "desc": "Cool CGI", "tags": ["CGI"], "prompt": "8k realistic action"}

def parse_meta(text):
    p = text.split("|")
    return {"title": p[0].strip(), "desc": p[1].strip(), "tags": p[2].split(","), "prompt": p[3].strip()}

def create_shaking_clip(image_path, duration=0.4):
    clip = ImageClip(image_path).set_duration(duration)
    def shake(get_frame, t):
        frame = get_frame(t)
        # Dynamic shake for that 'Realistic Action' feel
        sx, sy = random.randint(-20, 20), random.randint(-20, 20)
        return np.roll(np.roll(frame, sx, axis=1), sy, axis=0)
    return clip.fl(shake)

def build_video(meta):
    print(f"🎬 Creating: {meta['title']}")
    clips = []
    for i in range(12): # High-retention fast cuts
        url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,99999)}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        clips.append(create_shaking_clip(f"f{i}.jpg"))
    
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile("upload_ready.mp4", fps=30, codec="libx264", logger=None)
    return "upload_ready.mp4"

def upload_to_youtube(video_file, meta):
    with open('token.json', 'rb') as token: credentials = pickle.load(token)
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        'snippet': {
            'title': meta['title'],
            'description': meta['desc'],
            'tags': meta['tags'],
            'categoryId': '24',
            'defaultLanguage': 'en'
        },
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False},
        'recordingDetails': {
            'locationDescription': 'United States',
            'location': {'latitude': 37.0902, 'longitude': -95.7129}
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media).execute()
    print("✅ SUCCESS: Live on YouTube!")

if __name__ == "__main__":
    meta = get_metadata()
    path = build_video(meta)
    upload_to_youtube(path, meta)

