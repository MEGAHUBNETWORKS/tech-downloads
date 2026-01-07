import os, requests, random, time, wave, struct, json, math
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from PIL import Image, ImageEnhance, ImageFilter
from google.oauth2.credentials import Credentials

# --- CLOUD CONFIG ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1"), os.getenv("GEMINI_KEY_2"), os.getenv("GEMINI_KEY_3")]

def get_metadata():
    print("🧠 AI is choosing the legendary battle...")
    battles = [
        "Goku Ultra Instinct vs Gojo Satoru Infinity",
        "Saitama vs Boros Cosmic Battle",
        "Sukuna vs Mahoraga Shibuya",
        "Madara Uchiha vs Hashirama Senju"
    ]
    battle = random.choice(battles)
    prompt = f"Title | Desc | Tags | cinematic anime fight, {battle}, glowing energy auras, dark atmosphere, extreme action, 8k, hyper-realistic"
    
    random.shuffle(GEMINI_KEYS)
    for key in GEMINI_KEYS:
        if not key: continue
        try:
            client = Client(api_key=key)
            resp = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            p = resp.text.split("|")
            return {"t": p[0].strip(), "d": p[1].strip(), "tg": p[2].split(","), "pr": p[3].strip()}
        except: continue
    return {"t": f"{battle} Fight", "d": "Epic Battle", "tg": ["anime", "phonk"], "pr": battle}

def generate_audio(duration):
    print("🎵 Generating Phonk Bass Audio...")
    fps = 44100
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            hit = (i % (fps // 3)) < (fps // 12)
            val = max(-0.9, min(0.9, math.sin(2*math.pi*42*(i/fps))*10)) if hit else 0
            f.writeframesraw(struct.pack('<h', int(val * 32767)))

def build_video(meta):
    clips = []
    print(f"🖼️ Generating 12 Action Frames for: {meta['pr']}")
    for i in range(12):
        print(f"   -> Downloading Frame {i+1}/12...")
        url = f"https://image.pollinations.ai/prompt/{meta['pr'].replace(' ','%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,9999)}"
        try:
            with open(f"{i}.jpg", "wb") as f: f.write(requests.get(url, timeout=30).content)
            
            # Cinematic Grading
            img = Image.open(f"{i}.jpg")
            img = ImageEnhance.Contrast(img).enhance(1.8)
            img = ImageEnhance.Brightness(img).enhance(0.7).save(f"{i}.jpg")

            clip = ImageClip(f"{i}.jpg").set_duration(0.4)
            
            def anim(get_frame, t):
                frame = get_frame(t)
                if t < 0.1: # Speed Blur
                    frame = np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(radius=8)))
                s = 35 if t < 0.1 else 5 # Shake
                return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
            
            clips.append(clip.fl(anim))
        except Exception as e:
            print(f"⚠️ Frame {i} failed, skipping...")

    print("✂️ Stitching video together and adding motion blur...")
    video = concatenate_videoclips(clips, method="compose")
    generate_audio(video.duration)
    return video.set_audio(AudioFileClip("audio.wav").set_duration(video.duration))

def upload(file, meta):
    print("🚀 Connecting to YouTube API...")
    token_data = os.getenv("YT_TOKEN_DATA")
    if not token_data:
        print("❌ Error: YT_TOKEN_DATA secret is missing!")
        return

    creds = Credentials.from_authorized_user_info(json.loads(token_data))
    youtube = build("youtube", "v3", credentials=creds)
    
    body = {
        'snippet': {'title': meta['t'], 'description': meta['d'], 'tags': meta['tg'], 'categoryId': '24'},
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False},
        'recordingDetails': {'location': {'latitude': 37.09, 'longitude': -95.71}} # Target USA
    }
    
    print(f"📤 Uploading: {meta['t']}...")
    youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=MediaFileUpload(file)).execute()
    print("🏁 SUCCESS: Video is now Live on YouTube!")

if __name__ == "__main__":
    print("--- ⚡ STARTING FACTORY ⚡ ---")
    meta = get_metadata()
    video = build_video(meta)
    
    print("🎬 RENDERING MP4 (Watch progress below):")
    # logger='bar' ensures you see [###----] progress in GitHub logs
    video.write_videofile("out.mp4", fps=30, codec="libx264", audio_codec="aac", logger='bar')
    
    upload("out.mp4", meta)
    print("--- ⚡ FACTORY FINISHED ⚡ ---")
