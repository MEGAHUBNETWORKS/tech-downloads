import os, requests, random, time, wave, struct, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client

# --- AI CONFIG ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai_client = Client(api_key=GEMINI_KEY)

def get_gemini_metadata():
    """Gemini acts as the SEO Strategist for High-CPM Audience"""
    topic = random.choice(["Cyberpunk", "GTA 6 Realistic", "Marvel CGI", "Mythology"])
    
    for attempt in range(3):
        try:
            # Prompting for High-CTR "Epic" Metadata
            response = genai_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Generate viral SEO for a {topic} Short. Target: USA/Global audience. Format: Title | Description | Tags | Image Prompt"
            )
            parts = response.text.split("|")
            return {
                "title": parts[0].strip(),
                "desc": parts[1].strip(),
                "tags": parts[2].strip().split(","),
                "prompt": parts[3].strip()
            }
        except Exception as e:
            print(f"⚠️ Gemini busy, waiting 10s... {e}")
            time.sleep(10)

    return {"title": "Epic Scene #Shorts", "desc": "Cool CGI", "tags": ["CGI", "Epic"], "prompt": "Epic scene"}

def create_shaking_clip(image_path, duration=0.4):
    clip = ImageClip(image_path).set_duration(duration)
    def shake(get_frame, t):
        frame = get_frame(t)
        shift_x, shift_y = random.randint(-20, 20), random.randint(-20, 20)
        return np.roll(np.roll(frame, shift_x, axis=1), shift_y, axis=0)
    return clip.fl(shake)

def build_video(meta):
    print("🎬 Rendering Epic Fast-Cuts...")
    clips = []
    for i in range(10):
        url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        clips.append(create_shaking_clip(f"f{i}.jpg"))
    
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile("upload_ready.mp4", fps=30, codec="libx264", logger=None)
    return "upload_ready.mp4"

def upload_to_youtube(video_file, meta):
    with open('token.json', 'rb') as token:
        credentials = pickle.load(token)
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        'snippet': {
            'title': meta['title'],
            'description': meta['desc'],
            'tags': meta['tags'],
            'categoryId': '24', # Entertainment
            'defaultLanguage': 'en', # Force English
            'defaultAudioLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
            'embeddable': True
        },
        # TARGETING SETTINGS: Specific Location for High Revenue
        'recordingDetails': {
            'locationDescription': 'United States',
            'location': {
                'latitude': 37.0902,
                'longitude': -95.7129
            }
        }
    }
    
    print(f"🚀 Uploading to USA Audience: {meta['title']}")
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media).execute()
    print("✅ SUCCESS: 1M View Target Live!")

if __name__ == "__main__":
    meta = get_gemini_metadata()
    video_path = build_video(meta)
    upload_to_youtube(video_path, meta)

