import os, requests, random, time, wave, struct, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- VIDEO ENGINE ---
def create_shaking_clip(image_path, duration=0.4):
    clip = ImageClip(image_path).set_duration(duration)
    def shake(get_frame, t):
        frame = get_frame(t)
        shift_x, shift_y = random.randint(-20, 20), random.randint(-20, 20)
        return np.roll(np.roll(frame, shift_x, axis=1), shift_y, axis=0)
    return clip.fl(shake)

def build_video():
    prompt = "Epic cinematic 4k realistic action scene, high fidelity, " + random.choice(["Cyberpunk", "GTA 6", "Marvel"])
    clips = []
    for i in range(8):
        url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        clips.append(create_shaking_clip(f"f{i}.jpg"))
    
    final = concatenate_videoclips(clips, method="compose")
    # Write video silently to avoid GitHub hang
    final.write_videofile("upload_ready.mp4", fps=30, codec="libx264", logger=None)
    return "upload_ready.mp4", prompt

# --- UPLOADER ENGINE ---
def upload_to_youtube(video_file, video_title):
    if not os.path.exists('token.json'):
        print("❌ ERROR: token.json not found in GitHub!")
        return

    with open('token.json', 'rb') as token:
        credentials = pickle.load(token)

    youtube = build("youtube", "v3", credentials=credentials)
    
    request_body = {
        'snippet': {
            'title': f"{video_title} #Shorts #Epic",
            'description': 'Automated Epic Scene Render 2026',
            'categoryId': '24' # Entertainment
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    print(f"🚀 Uploading {video_file} to YouTube...")
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    ).execute()
    print("✅ SUCCESS: Video is now Live on YouTube!")

if __name__ == "__main__":
    path, title = build_video()
    upload_to_youtube(path, title)

