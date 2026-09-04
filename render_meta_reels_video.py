#!/usr/bin/env python3
"""
9:16 Meta Reels Ultra-High Quality Video Renderer
Generates 1080x1920 MP4 Video directly using Pillow and FFmpeg.
"""

import os
import sys
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_BIN = "/Users/silversurfer/Library/Python/3.9/lib/python/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-x86_64-v7.1"

WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 16.0 # 16 seconds
TOTAL_FRAMES = int(DURATION * FPS)

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
OUT_MP4_DOWNLOADS = os.path.join(DOWNLOADS_DIR, "sky_auto_services_meta_reel_9x16.mp4")
OUT_MP4_LOCAL = os.path.join(os.path.dirname(__file__), "meta_reels", "sky_auto_services_meta_reel_9x16.mp4")
OUT_MP4_PUBLIC = os.path.join(os.path.dirname(__file__), "public_html_local", "assets", "reels", "sky_auto_services_meta_reel_9x16.mp4")

os.makedirs(os.path.dirname(OUT_MP4_LOCAL), exist_ok=True)
os.makedirs(os.path.dirname(OUT_MP4_PUBLIC), exist_ok=True)

# Load Scene Images
SCENE_PATHS = [
    os.path.join(os.path.dirname(__file__), "meta_reels", "scene1_luxury_transport.jpg"),
    os.path.join(os.path.dirname(__file__), "meta_reels", "scene2_highway_hauler.jpg"),
    os.path.join(os.path.dirname(__file__), "meta_reels", "scene3_doorstep_delivery.jpg"),
    os.path.join(os.path.dirname(__file__), "meta_reels", "scene4_instant_quote.jpg"),
]

SCENE_IMAGES = []
for p in SCENE_PATHS:
    if os.path.exists(p):
        img = Image.open(p).convert("RGB")
        SCENE_IMAGES.append(img)
    else:
        # Fallback solid
        SCENE_IMAGES.append(Image.new("RGB", (WIDTH, HEIGHT), (20, 30, 50)))

# Fonts
FONT_DIR = "/System/Library/Fonts/Supplemental"
try:
    FONT_HEAD = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Black.ttf"), 64)
    FONT_HEAD_LARGE = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Black.ttf"), 72)
    FONT_SUB = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Bold.ttf"), 44)
    FONT_BADGE = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Bold.ttf"), 30)
    FONT_BRAND = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Bold.ttf"), 38)
    FONT_CTA = ImageFont.truetype(os.path.join(FONT_DIR, "Arial Black.ttf"), 50)
except Exception:
    FONT_HEAD = ImageFont.load_default()
    FONT_HEAD_LARGE = FONT_HEAD
    FONT_SUB = FONT_HEAD
    FONT_BADGE = FONT_HEAD
    FONT_BRAND = FONT_HEAD
    FONT_CTA = FONT_HEAD

# Pre-generate Top and Bottom Gradient Overlays
top_grad = Image.new("RGBA", (WIDTH, 480), (0, 0, 0, 0))
top_draw = ImageDraw.Draw(top_grad)
for y in range(480):
    alpha = int(220 * (1.0 - (y / 480.0) ** 1.3))
    top_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

bottom_grad = Image.new("RGBA", (WIDTH, 750), (0, 0, 0, 0))
bottom_draw = ImageDraw.Draw(bottom_grad)
for y in range(750):
    progress = y / 750.0
    alpha = int(240 * (progress ** 1.5))
    bottom_draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, alpha))

SCENES = [
    {
        "start": 0.0,
        "end": 3.5,
        "img_idx": 0,
        "badge": "NATIONWIDE AUTO TRANSPORT",
        "badge_color": (56, 189, 248),
        "headline_lines": ["DO NOT DRIVE YOUR", "CAR 2,000+ MILES! 🚗🛑"],
        "subtitles": [
            (0.0, 1.8, "Shipping your car across the US? 🇺🇸"),
            (1.8, 3.5, "DO NOT drive it yourself! 🛑")
        ]
    },
    {
        "start": 3.5,
        "end": 7.5,
        "img_idx": 1,
        "badge": "3,148+ VERIFIED CORRIDORS",
        "badge_color": (16, 185, 129),
        "headline_lines": ["SKIP THE ROAD TRIP", "NIGHTMARE! 🛣️💥"],
        "subtitles": [
            (3.5, 5.5, "Avoid rock chips, hotel bills & 35+ hrs driving!"),
            (5.5, 7.5, "100% Insured Open & Enclosed Fleet 🛡️")
        ]
    },
    {
        "start": 7.5,
        "end": 11.5,
        "img_idx": 2,
        "badge": "$0 UPFRONT DEPOSIT • TOP RATED",
        "badge_color": (245, 158, 11),
        "headline_lines": ["WHITE-GLOVE", "DOOR-TO-DOOR 🔑✨"],
        "subtitles": [
            (7.5, 9.5, "Delivered straight to your driveway! 🔑"),
            (9.5, 11.5, "$0 Upfront Deposit • 4.95 ★★★★★ Rating")
        ]
    },
    {
        "start": 11.5,
        "end": 16.0,
        "img_idx": 3,
        "badge": "SKYAUTOSERVICES.COM",
        "badge_color": (59, 130, 246),
        "headline_lines": ["GET YOUR INSTANT", "QUOTE IN 15 SECONDS ⏱️"],
        "subtitles": [
            (11.5, 13.5, "Calculate exact shipping in 15 seconds! ⚡"),
            (13.5, 16.0, "Tap Link Below To Lock Rate Today ⬇️")
        ]
    }
]

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_stroked_text(draw, pos, text, font, fill_color, stroke_color, stroke_width, align="center"):
    x, y = pos
    # Get text bounding box for alignment
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    if align == "center":
        draw_x = x - text_w // 2
    elif align == "right":
        draw_x = x - text_w
    else:
        draw_x = x
    
    # Draw thick stroke
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx*dx + dy*dy <= stroke_width*stroke_width and (dx != 0 or dy != 0):
                draw.text((draw_x + dx, y + dy), text, font=font, fill=stroke_color)
    draw.text((draw_x, y), text, font=font, fill=fill_color)

def generate_frame(t):
    # Find scene
    scene = SCENES[-1]
    for s in SCENES:
        if s["start"] <= t < s["end"]:
            scene = s
            break
            
    base_img = SCENE_IMAGES[scene["img_idx"]]
    scene_dur = scene["end"] - scene["start"]
    progress = (t - scene["start"]) / scene_dur

    # 1. Ken Burns Zoom & Pan
    zoom = 1.05 + progress * 0.08
    crop_w = int(base_img.width / zoom)
    crop_h = int(base_img.height / zoom)
    pan_y = int((progress - 0.5) * 60)
    
    left = max(0, (base_img.width - crop_w) // 2)
    top = max(0, min(base_img.height - crop_h, (base_img.height - crop_h) // 2 + pan_y))
    right = min(base_img.width, left + crop_w)
    bottom = min(base_img.height, top + crop_h)
    
    cropped = base_img.crop((left, top, right, bottom))
    frame = cropped.resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)

    # 2. Paste Gradients
    frame.paste(top_grad, (0, 0), top_grad)
    frame.paste(bottom_grad, (0, HEIGHT - 750), bottom_grad)

    draw = ImageDraw.Draw(frame)

    # 3. Top Header Bar
    draw_rounded_rect(draw, [60, 90, WIDTH - 60, 200], radius=24, fill=(15, 23, 42, 230), outline=(56, 189, 248), width=3)
    draw.text((100, 122), "SKY AUTO SERVICES", font=FONT_BRAND, fill=(56, 189, 248))
    draw.text((WIDTH - 100, 125), "★ 4.95 (1,284)", font=FONT_BADGE, fill=(245, 158, 11), anchor="ra")

    # 4. Category Badge Pill
    badge_w = 600
    badge_h = 64
    badge_x = (WIDTH - badge_w) // 2
    badge_y = 250
    draw_rounded_rect(draw, [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=32, fill=scene["badge_color"])
    bbox = draw.textbbox((0, 0), scene["badge"], font=FONT_BADGE)
    tw = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - tw // 2, badge_y + 14), scene["badge"], font=FONT_BADGE, fill=(0, 0, 0))

    # 5. Main Headline
    head_y = 390
    for line in scene["headline_lines"]:
        draw_stroked_text(draw, (WIDTH // 2, head_y), line, FONT_HEAD_LARGE, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=6)
        head_y += 85

    # 6. Hormozi Pop Subtitle Box
    sub_text = ""
    for sub_start, sub_end, txt in scene["subtitles"]:
        if sub_start <= t <= sub_end:
            sub_text = txt
            break
            
    if sub_text:
        sub_y = HEIGHT - 420
        draw_rounded_rect(draw, [60, sub_y - 30, WIDTH - 60, sub_y + 90], radius=24, fill=(0, 0, 0, 220), outline=(255, 255, 255), width=3)
        draw_stroked_text(draw, (WIDTH // 2, sub_y), sub_text, FONT_SUB, fill_color=(253, 224, 71), stroke_color=(0, 0, 0), stroke_width=4)

    # 7. Pulsing CTA Button in Scene 4
    if scene == SCENES[3]:
        pulse = 1.0 + math.sin(t * 8.0) * 0.03
        btn_w = int(760 * pulse)
        btn_h = int(120 * pulse)
        btn_x = (WIDTH - btn_w) // 2
        btn_y = HEIGHT - 240
        draw_rounded_rect(draw, [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=btn_h // 2, fill=(37, 99, 235), outline=(56, 189, 248), width=4)
        draw_stroked_text(draw, (WIDTH // 2, btn_y + 28), "GET INSTANT QUOTE ⚡", FONT_CTA, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=4)

    # 8. Rainbow Progress Bar
    progress_w = int((t / DURATION) * WIDTH)
    draw.rectangle([0, HEIGHT - 14, WIDTH, HEIGHT], fill=(40, 40, 50))
    for px in range(progress_w):
        r = int(56 + (236 - 56) * (px / WIDTH))
        g = int(189 - 100 * (px / WIDTH))
        b = int(248 - 50 * (px / WIDTH))
        draw.line([(px, HEIGHT - 14), (px, HEIGHT)], fill=(r, g, b))

    return frame

def main():
    print(f"🎬 Starting 9:16 Meta Reels Video Render ({WIDTH}x{HEIGHT} @ {FPS}fps, {DURATION}s)...")
    print(f"Using FFmpeg: {FFMPEG_BIN}")

    # FFmpeg command to read raw RGB frames and encode to pristine H.264 MP4 with upbeat synthetic audio track
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-", # stdin video
        "-f", "lavfi",
        "-i", f"aevalsrc=sin(2*PI*120*t)*0.2*exp(-5*mod(t\\,0.5))+sin(2*PI*240*t)*0.1*exp(-10*mod(t\\,0.25)):s=44100:d={DURATION}", # energetic electronic rhythm synth audio
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUT_MP4_DOWNLOADS
    ]

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for i in range(TOTAL_FRAMES):
        t = i / FPS
        frame = generate_frame(t)
        raw_bytes = frame.tobytes()
        process.stdin.write(raw_bytes)
        if (i + 1) % 60 == 0 or i == TOTAL_FRAMES - 1:
            print(f"Rendering frame {i+1}/{TOTAL_FRAMES} ({int((i+1)/TOTAL_FRAMES*100)}%)...")

    process.stdin.flush()
    try:
        process.stdin.close()
    except Exception:
        pass
    process.wait()

    if process.returncode != 0:
        print("FFmpeg process exited with code:", process.returncode)
        sys.exit(1)

    # Copy to local workspace locations as well
    import shutil
    shutil.copyfile(OUT_MP4_DOWNLOADS, OUT_MP4_LOCAL)
    shutil.copyfile(OUT_MP4_DOWNLOADS, OUT_MP4_PUBLIC)

    file_size_mb = os.path.getsize(OUT_MP4_DOWNLOADS) / (1024 * 1024)
    print("\n✅ Video rendering complete!")
    print(f"📁 Downloaded to: {OUT_MP4_DOWNLOADS} ({file_size_mb:.2f} MB)")
    print(f"📁 Local Copy: {OUT_MP4_LOCAL}")
    print(f"📁 Public Copy: {OUT_MP4_PUBLIC}")

if __name__ == "__main__":
    main()
