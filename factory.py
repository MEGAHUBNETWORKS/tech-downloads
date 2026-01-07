import os, random, math, wave, struct, requests, pickle
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -------------------------
# CATEGORY CONFIG
# -------------------------
CATEGORIES = {
    "cars": {"prompt": "ultra cinematic supercar, night, rain, neon lights, motion blur, high contrast, aggressive",
             "hook": ["NO LIMITS", "ILLEGAL SPEED", "900 HP"], "sound_freq": 45},
    "guns": {"prompt": "futuristic weapon charging energy, sparks, dark background, cinematic lighting, aggressive",
             "hook": ["MILITARY ONLY", "DO NOT TOUCH", "LIVE WEAPON"], "sound_freq": 60},
    "powers": {"prompt": "human hand glowing with energy, lightning aura, dark cinematic lighting, intense power",
               "hook": ["HUMAN LIMITS OFF", "POWER UNLOCKED", "UNSTABLE"], "sound_freq": 35},
    "tech": {"prompt": "high tech hud scan, cyberpunk interface, glowing data, dark futuristic style",
             "hook": ["AI SEES ALL", "SYSTEM ACTIVE", "TARGET LOCKED"], "sound_freq": 50}
}

CATEGORY = random.choice(list(CATEGORIES.keys()))
CFG = CATEGORIES[CATEGORY]

# -------------------------
# AUDIO GENERATION
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
# HOOK TEXT USING PILLOW
# -------------------------
def pillow_text_clip(text, duration=2.5, size=(1080,1920), fontsize=80):
    img = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
    w, h = draw.textsize(text, font=font)
    draw.text(((size[0]-w)/2,(size[1]-h)/2), text, font=font, fill=(255,255,255,255))
    tmp_file = "text_temp.png"
    img.save(tmp_file)
    return ImageClip(tmp_file).set_duration(duration)

# -------------------------
# ZOOM + SHAKE FX
# -------------------------
def zoom_shake_clip(clip):
    def zoom_shake(get_frame, t):
        frame = get_frame(t)
        s = 10
        frame = np.roll(np.roll(frame, random.randint(-s, s), axis=0), random.randint(-s, s), axis=1)
        return frame
    return clip.fl(zoom_shake).resize(lambda t: 1 + 0.03 * t)

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
        text_clip = pillow_text_clip(hook_text, duration=clip.duration, size=(clip.w, clip.h))
        clip = CompositeVideoClip([clip, text_clip])
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    generate_audio(video.duration)
    audio = AudioFileClip("audio.wav")
    final = video.set_audio(audio).set_duration(audio.duration)
    output_file = "short_ready.mp4"
    final.write_videofile(output_file, fps=30, codec="libx264", audio_codec="aac", logger=None)
    return output_file, hook_text

# -------------------------
# SEO + Thumbnail Generation
# -------------------------
def generate_seo(hook_text, category):
    seo = {}
    seo['title'] = f"{hook_text} | Epic {category.capitalize()} Shorts"
    seo['description'] = f"Watch this epic {category} moment! AI-generated cinematic content. #shorts #viral #{category}"
    seo_tags = {
        "cars":["supercar","speed","ai","viral","shorts","cinematic"],
        "guns":["weapons","ai","viral","shorts","action","cinematic"],
        "powers":["superpower","ai","viral","shorts","epic","cinematic"],
        "tech":["ai","futuristic","viral","shorts","cyberpunk","cinematic"]
    }
    seo['tags'] = seo_tags[category]
    return seo

def generate_thumbnail(category):
    prompt = f"{category} cinematic epic poster 4k"
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1280&height=720&seed={random.randint(1,99999)}"
    img_data = requests.get(url).content
    with open("thumbnail.jpg", "wb") as f:
        f.write(img_data)
    return "thumbnail.jpg"

# -------------------------
# UPLOAD TO YOUTUBE
# -------------------------
def upload_to_youtube(video_file, hook_text, category):
    if not os.path.exists("token.json"):
        print("⚠️ No YouTube token found. Skipping upload.")
        return
    with open("token.json", "rb") as t:
        creds = pickle.load(t)
    youtube = build("youtube", "v3", credentials=creds)
    seo = generate_seo(hook_text, category)
    thumb_file = generate_thumbnail(category)
    body = {
        "snippet": {"title": seo['title'], "description": seo['description'], "tags": seo['tags'], "categoryId": "24"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    res = req.execute()
    youtube.thumbnails().set(videoId=res['id'], media_body=MediaFileUpload(thumb_file)).execute()
    print(f"🚀 Uploaded: {seo['title']}")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    video_file, hook_text = build_video()
    upload_to_youtube(video_file, hook_text, CATEGORY)

