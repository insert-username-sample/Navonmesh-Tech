import os
import subprocess
import json
import math
import random
from studio.core.gpu_locker import gpu_task, vram_manager, GpuPriority

def get_audio_duration(audio_path):
    """Uses FFprobe to get the exact duration of the audio file in seconds."""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def generate_ffmpeg_zoom_pan(image_path, duration, output_path, resolution="3840:2160"):
    """
    Applies a dynamic 'Ken Burns' effect (slow zoom or pan) to a static image
    using FFmpeg, making it ready for 4K video concatenation.
    Default resolution: 3840x2160 (16:9 4K).
    """
    effect_type = random.choice(['zoom_in', 'zoom_out', 'pan_left', 'pan_right'])
    
    # Base filter for scaling ensuring height matches target resolution (e.g. 4K)
    w, h = resolution.split(":")
    base_vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    
    if effect_type == 'zoom_in':
        vf = f"{base_vf},zoompan=z='min(zoom+0.0015,1.15)':d={int(duration*30)}:x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':fps=30"
    elif effect_type == 'zoom_out':
        vf = f"{base_vf},zoompan=z='pzoom-0.0015':d={int(duration*30)}:x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':fps=30"
    elif effect_type == 'pan_left':
        vf = f"{base_vf},zoompan=z=1.1:x='max(0,x-1)':y='ih/2-(ih/zoom)/2':d={int(duration*30)}:fps=30"
    else: # pan_right
        vf = f"{base_vf},zoompan=z=1.1:x='min(iw-iw/zoom,x+1)':y='ih/2-(ih/zoom)/2':d={int(duration*30)}:fps=30"

    # Use NVENC for hardware acceleration (h264_nvenc for 16:9 master)
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', image_path,
        '-vf', vf, '-c:v', 'h264_nvenc', '-preset', 'fast', '-t', str(duration),
        '-pix_fmt', 'yuv420p', output_path
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

@gpu_task("Video Rendering (NVENC)", priority=GpuPriority.CRITICAL)
def assemble_video(audio_path, image_folder, final_output="final_render_4k.mp4"):
    """
    Calculates pacing, applies dynamic effects to images, and stitches them
    with the audio to create the final 4K video using NVENC.
    """
    total_duration = get_audio_duration(audio_path)
    images = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    if not images:
        print("Error: No images found.")
        return
    
    image_count = len(images)
    time_per_image = total_duration / image_count
    processed_clips = []
    
    print(f"[RENDER] Processing {image_count} images for 4K Master...")
    for idx, img in enumerate(images):
        clip_path = f"studio/temp/clip_{idx}.mp4"
        generate_ffmpeg_zoom_pan(img, time_per_image, clip_path)
        processed_clips.append(clip_path)

    concat_file = "studio/temp/concat_list.txt"
    with open(concat_file, 'w') as f:
        for clip in processed_clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    stitch_cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
        '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-shortest', final_output
    ]
    subprocess.run(stitch_cmd)

    # Cleanup
    for clip in processed_clips:
        if os.path.exists(clip): os.remove(clip)
    if os.path.exists(concat_file): os.remove(concat_file)

    print(f"[RENDER] ✅ 4K Master saved: {final_output}")
    return final_output

@gpu_task("9:16 Snippet Extraction", priority=GpuPriority.LOW)
def extract_9_16_snippet(input_video, output_video, start_time="00:00:00", duration="00:00:15"):
    """
    Extracts a 9:16 vertical snippet from a 16:9 master video.
    Uses center-cropping for now (Smart-AI-Crop with YOLOv8 can be added later).
    """
    print(f"[ENGINE] Extracting vertical snippet from {input_video}...")
    
    # 1. Calculate Crop (for 4K 3840x2160 -> 1215x2160 center crop)
    # The math for 4K 16:9 to 9:16 is (2160 * 9/16) = 1215.
    crop_vf = "crop=1215:2160:1312:0" # Center crop (3840/2 - 1215/2 = 1312)
    
    cmd = [
        'ffmpeg', '-y', '-ss', start_time, '-t', duration,
        '-i', input_video,
        '-vf', crop_vf,
        '-c:v', 'h264_nvenc', '-preset', 'fast', '-b:v', '10M',
        '-c:a', 'copy', output_video
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[ENGINE] ✅ 9:16 Snippet Exported: {output_video}")
    return output_video
