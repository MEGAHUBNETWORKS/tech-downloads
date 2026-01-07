import os, requests, random, time, wave, struct, pickle, math
import numpy as np
import librosa
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.genai import Client
from groq import Groq

# --- CONFIG ---
GEMINI_KEYS = [os.getenv("GEMINI_KEY_1")]
GROQ_KEY = os.getenv("GROQ_KEY")

def get_metadata():
    topic = random.choice(["Cyberpunk 2026", "Realistic GTA 6", "Viking Warrior", "Demon Samurai"])
    # [SEO Logic here - Uses Gemini/Groq to write viral title & prompt]
    # (Same as previous step to ensure unlimited uploads)
    return {"title": f"The {topic} #Shorts", "desc": "Aggressive CGI", "tags": ["Phonk", "CGI"], "prompt": f"8k realistic {topic}"}

# --- UPGRADED AUDIO: AGGRESSIVE BASS ---
def generate_aggressive_phonk(duration, filename="audio.wav"):
    """Generates heavy distorted 808 bass beats for Phonk energy"""
    fps = 44100
    with wave.open(filename, 'w') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(fps)
        for i in range(int(fps * duration)):
            # Pulse at 130 BPM (Aggressive Dance Tempo)
            pulse = (i % (fps // 2)) < (fps // 8) 
            if pulse:
                # Bass frequency + Distortion Clipping
                val = math.sin(2 * math.pi * 45 * (i / fps)) # 45Hz Sub
                val = max(-0.8, min(0.8, val * 4.0)) # Hard Overdrive
                f.writeframesraw(struct.pack('<h', int(val * 32767)))
            else:
                f.writeframesraw(struct.pack('<h', 0))

def build_video(meta):
    print("🎬 Producing Masterpiece...")
    clips = []
    # 12 Scenes at 0.4 seconds each = 4.8s loop (Perfect for high retention)
    for i in range(12): 
        url = f"https://image.pollinations.ai/prompt/{meta['prompt'].replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={random.randint(1,999)}"
        with open(f"f{i}.jpg", "wb") as f: f.write(requests.get(url).content)
        
        # Create Epic Shake
        clip = ImageClip(f"f{i}.jpg").set_duration(0.4)
        def shake(get_frame, t):
            frame = get_frame(t)
            s = 25 # Intensity
            return np.roll(np.roll(frame, random.randint(-s, s), axis=1), random.randint(-s, s), axis=0)
        clips.append(clip.fl(shake))
    
    final_video = concatenate_videoclips(clips, method="compose")
    generate_aggressive_phonk(final_video.duration)
    
    # Syncing audio and export
    audio = AudioFileClip("audio.wav")
    final_video = final_video.set_audio(audio)
    final_video.write_videofile("upload_ready.mp4", fps=30, codec="libx264", logger=None)
    return "upload_ready.mp4"

def upload_to_youtube(file, meta):
    # [Uploader logic remains same with US targeting]
    pass

if __name__ == "__main__":
    m = get_metadata()
    v = build_video(m)
    upload_to_youtube(v, m)

