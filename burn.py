import os
import subprocess
import sys

def hard_sub_videos_in_folder(folder_path):
    print(f"Processing folder: {folder_path}")
    for root, _, files in os.walk(folder_path):  # Walk through all subfolders
        for subtitle_file in files:
            if subtitle_file.endswith(".en.vtt") or subtitle_file.endswith(".en-SG.vtt"):
                print(f"Found subtitle file: {subtitle_file} in {root}")
                video_file = subtitle_file.replace(".en.vtt", ".mp4").replace(".en-SG.vtt", ".mp4")
                if os.path.exists(os.path.join(root, video_file)):
                    output_file = f"temp_{video_file}"
                    print(f"Matching video file found: {video_file}")
                    try:
                        # Run ffmpeg in Docker to hardcode subtitles
                        subprocess.run([
                            "docker", "run", "--rm", "-v", f"{root}:/data", "byam/ffmpeg",
                            "-i", f"/data/{video_file}", "-vf", f"subtitles=/data/{subtitle_file}:force_style='Alignment=6'",
                            "-c:a", "copy", f"/data/{output_file}"
                        ], check=True)
                        print(f"Hardsub completed for {video_file}")
                        # Replace original files with hard-subbed video
                        os.remove(os.path.join(root, video_file))
                        os.remove(os.path.join(root, subtitle_file))
                        os.rename(os.path.join(root, output_file), os.path.join(root, video_file))
                        print(f"Rename done for {video_file}")

                    except Exception as e:
                        print(f"Error processing {video_file}: {e}")

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        hard_sub_videos_in_folder(folder_path)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(1)
