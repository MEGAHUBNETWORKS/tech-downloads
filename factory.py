# ===========================================
# ULTIMATE VIRAL SHORTS FACTORY + AUTOMATIC YOUTUBE UPLOAD
# All growth optimizations applied
# ===========================================

import os, random, math, wave, struct, requests, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -------------------------
# CATEGORY CONFIG
# -------------------------
CATEGORIES = {
    "cars": {
        "prompt": "ultra cinematic close-up supercar, night, rain, neon lights, motion blur, high contrast, aggressive",
        "hook": ["NO LIMITS", "ILLEGAL SPEED", "900 HP"],
        "sound_freq": 45
    },
    "guns": {
        "prompt": "futuristic weapon charging energy, sparks, dark background, cinematic lighting, aggressive",
        "hook": ["MILITARY ONLY", "DO NOT TOUCH", "LIVE WEAPON"],
        "sound_freq": 60
    },
    "powers": {
        "prompt": "human hand glowing with energy, lightning aura, dark cinematic lighting, intense power",
        "hook": ["HUMAN LIMITS OFF", "POWER UNLOCKED", "UNSTABLE"],
        "sound_freq": 35
    },
    "tech": {
        "prompt": "high tech hud scan, cyberpunk interface, glowing data, dark futuristic style",
        "hook": ["AI SEES ALL", "SYSTEM ACTIVE", "TARGET LOCKED"],
        "sound_freq": 50
    }
}

CATEGORY = random.choice(list(CATEGORIES.keys()))
CFG = CATEGORIES[CATEGORY]

# -------------------------
# AUDIO GENERATION (AGGRESSIVE + SILENCE)
# -------------------------
def generate_audio(duration=23, filename="audio.wav"):
    fps = 44100
    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fps)

        for i in range(int(duration * fps)):
            t = i / fps
            val = 0 if t < 1.5 else max(-0.8, min(0.8, math.sin(2 * math.pi * CFG["sound_freq"] * t) * 4))
            f.writeframesraw(struct.pack("<h", int(val * 32767)))

# -------------------------
# IMAGE FETCH
# -------------------------
def get_image(prompt, idx):
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1080&height=1920&seed={random.randint(1,99999)}"
    img = requests.get(url).content
    name = f"frame_{idx}.jpg"
    with open(name, "wb") as f:
        f.write(img)
    return name

# -------------------------
# HOOK TEXT + MOTION FX
# -------------------------
def zoom_shake_clip(clip):
    def zoom_shake(get_frame, t):
        frame = get_frame(t)
        zoom = 1 + 0.03 * t
        frame = np.array(frame)
        # Slight shake
        s = 10
        frame = np.roll(np.roll(frame, random.randint(-s, s), axis=0), random.randint(-s, s), axis=1)
        return frame
    return clip.fl(zoom_shake).resize(lambda t: 1 + 0.03 * t)

def add_hook_text(clip, text):
    txt = TextClip(text, fontsize=80, color='white', font='Arial-Bold', stroke_color='black', stroke_width=3)
    txt = txt.set_duration(clip.duration).set_pos('center')
    return CompositeVideoClip([clip, txt])

# -------------------------
# VIDEO BUILD
# -------------------------
def build_video():
    clips = []
    hook_text = random.choice(CFG["hook"])

    for i in range(8):
        img = get_image(CFG["prompt"], i)
        clip = ImageClip(img).set_duration(2.5)
        clip = zoom_shake_clip(clip)
        # Hook text on all clips for max retention
        clip = add_hook_text(clip, hook_text)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    generate_audio(video.duration)
    audio = AudioFileClip("audio.wav")

    final = video.set_audio(audio).set_duration(audio.duration)
    output_file = "short_ready.mp4"
    final.write_videofile(output_file, fps=30, codec="libx264", audio_codec="aac", logger=None)

    return output_file, hook_text

# -------------------------
# DYNAMIC THUMBNAIL
# -------------------------
def generate_thumbnail(category):
    prompt = CATEGORIES[category]["prompt"] + ", cinematic poster, epic composition, 4k"
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1280&height=720&seed={random.randint(1,99999)}"
    response = requests.get(url).content
    thumb_file = "thumbnail.jpg"
    with open(thumb_file, "wb") as f:
        f.write(response)
    return thumb_file

# -------------------------
# CATEGORY-BASED SEO
# -------------------------
def generate_seo(category, hook_text):
    seo = {}
    seo_titles = {
        "cars": [f"{hook_text} | Supercar Moment", f"{hook_text} | Illegal Speed", f"{hook_text} | 900HP Action"],
        "guns": [f"{hook_text} | Secret Weapon", f"{hook_text} | Military Tech", f"{hook_text} | Live Fire"],
        "powers": [f"{hook_text} | Unstoppable Power", f"{hook_text} | Human Limit Removed", f"{hook_text} | Superhuman Moment"],
        "tech": [f"{hook_text} | AI Revealed", f"{hook_text} | Futuristic Tech", f"{hook_text} | Cyberpunk Moment"]
    }
    seo['title'] = random.choice(seo_titles[category])
    seo['description'] = (
        f"Watch this epic {category} moment that was never meant to be seen.\n"
        f"Stay until the end for maximum impact.\n\n"
        f"#shorts #viral #{category} #cinematic #ai"
    )
    seo_tags = {
        "cars": ["supercar","speed","viral shorts","cinematic","ai generated","epic","future tech"],
        "guns": ["weapon","military","viral shorts","cinematic","ai generated","tech","power"],
        "powers": ["superpower","human limit","viral shorts","cinematic","ai generated","energy","epic"],
        "tech": ["ai","futuristic","viral shorts","cinematic","technology","epic","future"]
    }
    seo['tags'] = seo_tags[category]
    return seo

# -------------------------
# YOUTUBE UPLOAD
# -------------------------
def upload_to_youtube(video_file, hook_text, category):
    if not os.path.exists('token.json'):
        print("⚠️ No YouTube credentials (token.json) found. Skipping upload.")
        return

    with open('token.json', 'rb') as t:
        credentials = pickle.load(t)

    youtube = build("youtube", "v3", credentials=credentials)
    seo = generate_seo(category, hook_text)
    thumbnail_file = generate_thumbnail(category)

    body = {
        'snippet': {
            'title': seo['title'],
            'description': seo['description'],
            'tags': seo['tags'],
            'categoryId': '24',
            'defaultLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        },
        'recordingDetails': {
            'locationDescription': 'USA',
            'location': {'latitude': 37.09, 'longitude': -95.71}
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media)
    response = request.execute()
    youtube.thumbnails().set(videoId=response['id'], media_body=MediaFileUpload(thumbnail_file)).execute()
    print("🚀 Video uploaded with dynamic thumbnail and full growth SEO!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    video_file, hook_text = build_video()
    upload_to_youtube(video_file, hook_text, CATEGORY)
def generate_thumbnail(category):
    prompt = CATEGORIES[category]["prompt"] + ", cinematic poster, epic composition, 4k"
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1280&height=720&seed={random.randint(1,99999)}"
    response = requests.get(url).content
    thumb_file = "thumbnail.jpg"
    with open(thumb_file, "wb") as f:
        f.write(response)
    return thumb_file

# -------------------------
# CATEGORY-BASED SEO
# -------------------------
def generate_seo(category, hook_text):
    seo = {}
    seo_titles = {
        "cars": [f"{hook_text} | Supercar Moment", f"{hook_text} | Illegal Speed", f"{hook_text} | 900HP Action"],
        "guns": [f"{hook_text} | Secret Weapon", f"{hook_text} | Military Tech", f"{hook_text} | Live Fire"],
        "powers": [f"{hook_text} | Unstoppable Power", f"{hook_text} | Human Limit Removed", f"{hook_text} | Superhuman Moment"],
        "tech": [f"{hook_text} | AI Revealed", f"{hook_text} | Futuristic Tech", f"{hook_text} | Cyberpunk Moment"]
    }
    seo['title'] = random.choice(seo_titles[category])

    seo['description'] = (
        f"Watch this epic {category} moment that was never meant to be seen.\n"
        f"Stay until the end for maximum impact.\n\n"
        f"#shorts #viral #{category} #cinematic #ai"
    )

    seo_tags = {
        "cars": ["supercar","speed","viral shorts","cinematic","ai generated","epic","future tech"],
        "guns": ["weapon","military","viral shorts","cinematic","ai generated","tech","power"],
        "powers": ["superpower","human limit","viral shorts","cinematic","ai generated","energy","epic"],
        "tech": ["ai","futuristic","viral shorts","cinematic","technology","epic","future"]
    }
    seo['tags'] = seo_tags[category]
    return seo

# -------------------------
# YOUTUBE UPLOAD
# -------------------------
def upload_to_youtube(video_file, hook_text, category):
    if not os.path.exists('token.json'):
        print("⚠️ No YouTube credentials (token.json) found. Skipping upload.")
        return

    with open('token.json', 'rb') as t:
        credentials = pickle.load(t)

    youtube = build("youtube", "v3", credentials=credentials)

    seo = generate_seo(category, hook_text)
    thumbnail_file = generate_thumbnail(category)

    body = {
        'snippet': {
            'title': seo['title'],
            'description': seo['description'],
            'tags': seo['tags'],
            'categoryId': '24',
            'defaultLanguage': 'en'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        },
        'recordingDetails': {
            'locationDescription': 'USA',
            'location': {'latitude': 37.09, 'longitude': -95.71}
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media)
    response = request.execute()

    youtube.thumbnails().set(videoId=response['id'], media_body=MediaFileUpload(thumbnail_file)).execute()
    print("🚀 Video uploaded with dynamic thumbnail and optimized SEO!")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    video_file, hook_text = build_video()
    upload_to_youtube(video_file, hook_text, CATEGORY)
    print(f"💥 HOOK TEXT: {random.choice(CFG['hook'])}")
    print(f"✅ VIDEO OUTPUT: {output_file}")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    build_video()

