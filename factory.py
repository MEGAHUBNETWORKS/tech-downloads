# =========================
# AWESOME MOMENT SHORTS FACTORY
# RETENTION OPTIMIZED, VIRAL-FRIENDLY
# =========================

import os, random, math, wave, struct, requests
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

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
# AUDIO (AGGRESSIVE + SILENCE)
# -------------------------
def generate_audio(duration=23, filename="audio.wav"):
    fps = 44100
    with wave.open(filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fps)

        for i in range(int(duration * fps)):
            t = i / fps

            # silence first 1.5 seconds for retention
            if t < 1.5:
                val = 0
            else:
                beat = math.sin(2 * math.pi * CFG["sound_freq"] * t)
                val = max(-0.8, min(0.8, beat * 4))

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
# MOTION (ZOOM FOR RETENTION)
# -------------------------
def zoom_effect(clip):
    return clip.resize(lambda t: 1 + 0.03 * t)

# -------------------------
# VIDEO BUILD
# -------------------------
def build_video():
    clips = []

    for i in range(8):  # few clips = clean and hypnotic
        img = get_image(CFG["prompt"], i)
        clip = ImageClip(img).set_duration(2.5)
        clip = zoom_effect(clip)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    generate_audio(video.duration)
    audio = AudioFileClip("audio.wav")

    final = video.set_audio(audio).set_duration(audio.duration)
    output_file = "short_ready.mp4"
    final.write_videofile(
        output_file,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        logger=None
    )

    # Display hook for overlay or SEO
    print(f"🔥 CATEGORY: {CATEGORY.upper()}")
    print(f"💥 HOOK TEXT: {random.choice(CFG['hook'])}")
    print(f"✅ VIDEO OUTPUT: {output_file}")

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    build_video()

