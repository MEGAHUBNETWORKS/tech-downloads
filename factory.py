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
    "cars": {"prompt": "ultra cinematic close-up supercar, night, rain, neon lights, motion blur, high contrast, aggressive",
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
# RUN (simplified YouTube upload can be added later)
# -------------------------
if __name__ == "__main__":
    build_video()
    
