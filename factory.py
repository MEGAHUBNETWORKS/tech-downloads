import os, requests, random, time, wave, struct
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, vfx

# --- CONFIG ---
# Ensure these are in your GitHub Secrets
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_epic_prompt():
    themes = [
        "Cyberpunk samurai deflective sparks, neon rain, hyper-realistic",
        "GTA 6 style supercar mid-air explosion, motion blur, 8k render",
        "Marvel Thor landing with massive lightning cracks, realistic textures",
        "Ancient warrior standing against a dragon, cinematic fire lighting"
    ]
    return random.choice(themes)

def create_shaking_clip(image_path, duration=0.5):
    """ Creates a 'Camera Shake' effect for that Epic feeling """
    clip = ImageClip(image_path).set_duration(duration)
    
    # Shake effect: Randomly crop and move the frame slightly
    def shake(get_frame, t):
        frame = get_frame(t)
        # Shift pixels slightly to simulate vibration
        shift_x = random.randint(-15, 15)
        shift_y = random.randint(-15, 15)
        return np.roll(np.roll(frame, shift_x, axis=1), shift_y, axis=0)

    return clip.fl(shake)

def build_epic_short():
    print("🚀 Starting Epic Video Production...")
    prompt = get_epic_prompt()
    clips = []
    
    # Generate 8 High-Action frames for "Fast Cuts"
    for i in range(8):
        print(f"Generating Frame {i+1}/8...")
        seed = random.randint(1, 100000)
        url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1080&height=1920&model=flux&seed={seed}"
        
        img_data = requests.get(url).content
        fname = f"f_{i}.jpg"
        with open(fname, "wb") as f:
            f.write(img_data)
            
        # Add to timeline with a shake effect
        clips.append(create_shaking_clip(fname, duration=0.4))

    # Stitch the fast-cuts together
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Generate the Bass-Boosted 'Thump' Audio
    generate_bass_audio(duration=final_video.duration)
    
    final_video = final_video.set_audio(AudioFileClip("audio.wav"))
    final_video.write_videofile("upload_ready.mp4", fps=30, codec="libx264")
    print("✅ Epic Short Ready for Upload!")

def generate_bass_audio(duration):
    """ Generates a Heavy 808 Phonk-style Bass Beat """
    with wave.open("audio.wav", 'w') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(44100)
        for i in range(int(44100 * duration)):
            # Create a rhythmic bass pulse every 0.4 seconds to match the cuts
            if (i % 17640 < 4000): # Bass Thump
                val = int(32767 * 0.8)
            else:
                val = 0
            f.writeframesraw(struct.pack('<h', val))
            f.writeframesraw(struct.pack('<h', val))

if __name__ == "__main__":
    build_epic_short()

