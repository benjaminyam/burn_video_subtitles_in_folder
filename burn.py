import os
import subprocess
import sys
import re

def sanitize_filename(filename):
    """Replace or remove unsupported characters in the filename."""
    return re.sub(r'[^\w\-.]', '_', filename)

def hard_sub_videos_in_folder(folder_path):
    print(f"Processing folder: {folder_path}")
    for root, _, files in os.walk(folder_path):  # Walk through all subfolders
        for file in files:
            file_path = os.path.join(root, file)
            
            # Delete any .mp4.tmp files
            if file.startswith("tmp_") and file.endswith(".mp4"):
                print(f"Deleting temporary file: {file_path}")
                os.remove(file_path)
                continue
            
            # Process subtitle files
            if file.endswith(".en.vtt") or file.endswith(".en-SG.vtt"):
                print(f"Found subtitle file: {file} in {root}")
                video_file = file.replace(".en.vtt", ".mp4").replace(".en-SG.vtt", ".mp4")
                video_path = os.path.join(root, video_file)
                
                # Sanitize file names
                sanitized_video_file = sanitize_filename(video_file)
                sanitized_subtitle_file = sanitize_filename(file)
                sanitized_video_path = os.path.join(root, sanitized_video_file)
                sanitized_subtitle_path = os.path.join(root, sanitized_subtitle_file)

                # Rename files to sanitized names if necessary
                if video_file != sanitized_video_file and os.path.exists(video_path):
                    os.rename(video_path, sanitized_video_path)
                    print(f"Renamed video file to: {sanitized_video_file}")
                if file != sanitized_subtitle_file and os.path.exists(file_path):
                    os.rename(file_path, sanitized_subtitle_path)
                    print(f"Renamed subtitle file to: {sanitized_subtitle_file}")
                
                # Check if sanitized video file exists
                if os.path.exists(sanitized_video_path):
                    output_file = f"tmp_{sanitized_video_file}"
                    output_path = os.path.join(root, output_file)
                    print(f"Matching video file found: {sanitized_video_file}")
                    try:
                        # Run ffmpeg in Docker to hardcode subtitles
                        subprocess.run([
                            "docker", "run", "--rm", "-v", f"{root}:/data", "byam/ffmpeg",
                            "-i", f"/data/{sanitized_video_file}", "-vf", f"subtitles=/data/{sanitized_subtitle_file}:force_style='Alignment=6'",
                            "-c:a", "copy", f"/data/{output_file}"
                        ], check=True)
                        print(f"Hardsub completed for {sanitized_video_file}")
                        
                        # Replace original files with hard-subbed video
                        os.remove(sanitized_video_path)
                        os.remove(sanitized_subtitle_path)
                        os.rename(output_path, sanitized_video_path)
                        print(f"Rename done for {sanitized_video_file}")

                    except Exception as e:
                        print(f"Error processing {sanitized_video_file}: {e}")

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        hard_sub_videos_in_folder(folder_path)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(1)