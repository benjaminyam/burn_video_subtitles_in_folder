import os
import subprocess
import sys

def hard_sub_videos_in_folder(folder_path):
    print(f"Processing folder: {folder_path}")
    for root, _, files in os.walk(folder_path):  # Walk through all subfolders
        for file in files:
            file_path = os.path.join(root, file)
            
            # Process subtitle files
            if file.endswith(".en.vtt") or file.endswith(".en-SG.vtt"):
                print(f"Found subtitle file: {file} in {root}")
                video_file = file.replace(".en.vtt", ".mp4").replace(".en-SG.vtt", ".mp4")
                video_path = os.path.join(root, video_file)
                
                if os.path.exists(video_path):
                    output_file = f"{video_file}.tmp"
                    output_path = os.path.join(root, output_file)
                    print(f"Matching video file found: {video_file}")
                    try:
                        # Run ffmpeg in Docker to hardcode subtitles
                        subprocess.run([
                            "docker", "run", "--rm", "-v", f"{root}:/data", "byam/ffmpeg",
                            "-i", f"/data/{video_file}", "-vf", f"subtitles=/data/{file}:force_style='Alignment=6'",
                            "-c:a", "copy", f"/data/{output_file}"
                        ], check=True)
                        print(f"Hardsub completed for {video_file}")
                        
                        # Replace original files with hard-subbed video
                        os.remove(video_path)
                        os.remove(file_path)
                        os.rename(output_path, video_path)
                        print(f"Rename done for {video_file}")

                    except Exception as e:
                        print(f"Error processing {video_file}: {e}")
            
            # Delete any .mp4.tmp files
            elif file.endswith(".mp4.tmp"):
                print(f"Deleting temporary file: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        hard_sub_videos_in_folder(folder_path)
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(1)
