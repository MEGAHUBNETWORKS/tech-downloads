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
    """Gemini acts as the SEO Strategist and Writer"""
    # Gemini generates a unique, interesting scene idea
    topic = random.choice(["Cyberpunk", "GTA 6 Realistic", "Marvel CGI", "Mythology"])
    
    # Prompting Gemini for SEO-optimized Title, Description, and Tags
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Create a viral YouTube Short title, a 2-sentence description with 5 hashtags, and an image prompt for an epic {topic} scene. Format as: Title | Desc | Prompt"
    )
    
    parts = response.text.split("|")
    return {
        "title": parts[0].strip(),
        "desc": parts[1].strip(),
        "prompt": parts[2].strip()
    }

def create_shaking_clip(image_path, duration=0.4):
    clip = ImageClip(image_path).set_duration(duration)
    def shake(get_frame, t):
        frame = get_frame(t)
        shift_x, shift_y = random.randint(-25, 25), random.randint(-25, 25)
        return np.roll(np.roll(frame, shift_x, axis=1), shift_y, axis=0)
    return clip.fl(shake)

def build_video(meta):
    print(f"🎬 Producing: {meta['title']}")
    clips = []
    for i in range(12): # Fast cuts for high retention
        seed = random.randint(1, 99999)
        url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={seed}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        clips.append(create_shaking_clip(f"f{i}.jpg"))
    
    final = concatenate_videoclips(clips, method="compose")
    # Using 'logger=None' to prevent GitHub hang
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
            'categoryId': '24'
        },
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
    }
    
    print("🚀 Uploading with SEO Metadata...")
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    print("✅ SUCCESS: Video is Live!")

if __name__ == "__main__":
    meta = get_gemini_metadata()
    video_path = build_video(meta)
    upload_to_youtube(video_path, meta)

