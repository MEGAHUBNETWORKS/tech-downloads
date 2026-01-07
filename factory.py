import os, requests, random, time, wave, struct, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- 2026 EPIC ENGINE ---
def create_shaking_clip(image_path, duration=0.4):
    clip = ImageClip(image_path).set_duration(duration)
    def shake(get_frame, t):
        frame = get_frame(t)
        shift_x, shift_y = random.randint(-20, 20), random.randint(-20, 20)
        return np.roll(np.roll(frame, shift_x, axis=1), shift_y, axis=0)
    return clip.fl(shake)

def generate_bass_audio(duration):
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(44100)
        for i in range(int(44100 * duration)):
            val = int(32767 * 0.9) if (i % 17640 < 5000) else 0
            f.writeframesraw(struct.pack('<h', val) * 2)

def build_video():
    prompt = "Epic cinematic 4k realistic action scene, high fidelity, " + random.choice(["Cyberpunk", "Medieval", "GTA 6", "Space"])
    clips = []
    for i in range(10): # 10 fast-cuts
        url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1080&height=1920&seed={random.randint(1,999)}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        clips.append(create_shaking_clip(f"f{i}.jpg"))
    
    final = concatenate_videoclips(clips, method="compose")
    generate_bass_audio(final.duration)
    # logger=None PREVENTS THE "STUCK" HANG IN GITHUB ACTIONS
    final.set_audio(AudioFileClip("audio.wav")).write_videofile("upload.mp4", fps=30, codec="libx264", logger=None)
    return "upload.mp4", prompt

# --- AUTO UPLOADER ---
def upload_to_youtube(file_path, title):
    with open('token.json', 'rb') as t: creds = pickle.load(t)
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        'snippet': {'title': title, 'description': '#Shorts #Epic #CGI', 'categoryId': '24'},
        'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}
    }
    youtube.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(file_path)).execute()
    print("🚀 Video Uploaded!")

if __name__ == "__main__":
    path, title = build_video()
    upload_to_youtube(path, title)

