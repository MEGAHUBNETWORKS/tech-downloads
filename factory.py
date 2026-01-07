import os, requests, random, time, wave, struct, json, math
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq
from PIL import Image, ImageEnhance, ImageFilter
from google.oauth2.credentials import Credentials

# --- KEYS ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1"), os.getenv("GEMINI_KEY_2"), os.getenv("GEMINI_KEY_3")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    battles = ["Goku vs Gojo", "Saitama vs Boros", "Sukuna vs Mahoraga", "Madara vs Hashirama"]
    battle = random.choice(battles)
    prompt = f"Title | Desc | Tags | cinematic anime fight, 8k, {battle}, glowing energy auras, dark atmosphere, action scene"
    
    random.shuffle(GEMINI_KEYS)
    for key in GEMINI_KEYS:
        if key:
            try:
                c = Client(api_key=key)
                r = c.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                p = r.text.split("|")
                return {"t":p[0],"d":p[1],"tg":p[2].split(","),"pr":p[3]}
            except: continue
    return {"t":f"{battle} Fight","d":"Epic","tg":["anime"],"pr":battle}

def generate_audio(duration):
    fps = 44100
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            hit = (i % (fps // 3)) < (fps // 12)
            val = max(-0.9, min(0.9, math.sin(2*math.pi*42*(i/fps))*10)) if hit else 0
            f.writeframesraw(struct.pack('<h', int(val * 32767)))

def build_video(meta):
    clips = []
    for i in range(12):
        url = f"https://image.pollinations.ai/prompt/{meta['pr'].replace(' ','%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        with open(f"{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        
        # Color Grading
        img = Image.open(f"{i}.jpg")
        img = ImageEnhance.Contrast(img).enhance(1.6)
        img = ImageEnhance.Brightness(img).enhance(0.7).save(f"{i}.jpg")

        clip = ImageClip(f"{i}.jpg").set_duration(0.4)
        def anim(get_frame, t):
            frame = get_frame(t)
            # Motion Blur + Zoom
            if t < 0.1:
                img_f = Image.fromarray(frame).filter(ImageFilter.GaussianBlur(radius=8))
                frame = np.array(img_f)
            s = 30 if t < 0.1 else 5
            return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
        clips.append(clip.fl(anim))

    video = concatenate_videoclips(clips, method="compose")
    generate_audio(video.duration)
    return video.set_audio(AudioFileClip("audio.wav").set_duration(video.duration))

def upload(file, meta):
    token_data = os.getenv("YT_TOKEN_DATA")
    if not token_data: return print("❌ No Token Found")
    
    creds = Credentials.from_authorized_user_info(json.loads(token_data))
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        'snippet':{'title':meta['t'],'description':meta['d'],'tags':meta['tg'],'categoryId':'24'},
        'status':{'privacyStatus':'public','selfDeclaredMadeForKids':False},
        'recordingDetails':{'location':{'latitude':37.09,'longitude':-95.71}}
    }
    youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=MediaFileUpload(file)).execute()

if __name__ == "__main__":
    m = get_metadata()
    v = build_video(m)
    v.write_videofile("out.mp4", fps=30, codec="libx264", logger=None)
    upload("out.mp4", m)
