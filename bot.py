import os, asyncio, random, math, requests, datetime, pickle
import numpy as np
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx as vfx
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from googleapiclient.discovery import build

# --- MASTER CONFIG ---
PEXELS_API = os.getenv('PEXELS_API_KEY')
LINK = "https://link-center.net/2645038/VuBhMuTSWyaC"

def auto_engage_comments(video_id):
    """Likes and replies to the first batch of comments to explode the algorithm."""
    try:
        with open("credentials.storage", "rb") as f:
            credentials = pickle.load(f)
        youtube = build("youtube", "v3", credentials=credentials)
        
        # Search for comments
        results = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=10).execute()
        
        replies = ["🔥", "💀", "W", "💯", "Check the link in bio for more!", "Absolute beast!"]
        
        for item in results.get('items', []):
            comment_id = item['snippet']['topLevelComment']['id']
            # Reply to comment
            youtube.comments().insert(
                part="snippet",
                body={
                    "snippet": {
                        "parentId": comment_id,
                        "textOriginal": random.choice(replies)
                    }
                }
            ).execute()
            print(f"💬 Replied to comment on {video_id}")
    except Exception as e:
        print(f"⚠️ Engagement skip: {e}")

# [Previous get_global_target_time, apply_alpha_grading, apply_kasmandra_vfx, stalk_trending_hashtags logic remains]

async def run_engine():
    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")

    # 1. SELECT NICHE & STALK TAGS
    niche = random.choice(['JOHN_WICK', 'FAST_FURIOUS', 'MARVEL'])
    trending_tags = stalk_trending_hashtags(niche)

    # 2. FETCH HIGH-DETAIL ASSETS & PRODUCE VIDEO
    # [Video production logic with 30,000k bitrate and Teal & Orange grading...]

    # 3. GLOBAL DEPLOY
    video = LocalVideo(file_path="final.mp4")
    video.set_title(f"{niche} 💀 // GTA 6 GRAPHICS {trending_tags}")
    uploaded = channel.upload_video(video)
    video_id = uploaded.id
    
    # 4. START AUTO-ENGAGEMENT
    # We wait 60 seconds for the first viewers to arrive
    print("⏳ Waiting for initial engagement...")
    await asyncio.sleep(60)
    auto_engage_comments(video_id)
    
    print(f"🌍 GLOBAL DOMINATION ACTIVE: https://youtu.be/{video_id}")

if __name__ == "__main__":
    asyncio.run(run_engine())
    
