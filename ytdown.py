import os
import subprocess
from pytube import YouTube
import requests
import re


def get_playlist_id(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        print("Error: Playlist ID not found in URL.")
        return None


def get_video_links(playlist_id):
    try:
        res = requests.get(f"https://youtube.com/playlist?list={playlist_id}")
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

    video_links = re.findall(r'watch\?v=([a-zA-Z0-9_-]+)', res.text)
    return ["https://youtube.com/watch?v=" + link for link in video_links]


def download_videos(links, resolution, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for link in links:
        try:
            yt = YouTube(link)
            video_title = yt.title
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()
            if video_stream:
                print(f"Downloading '{video_title}'...")
                video_stream.download(save_path)
                print(f"Downloaded '{video_title}'")
            else:
                print(f"No available {resolution} stream for '{video_title}'")
        except Exception as e:
            print(f"Error downloading '{link}': {e}")


def main():
    print("WELCOME TO PLAYLIST DOWNLOADER DEVELOPED BY - www.github.com/KunalG932")

    playlist_url = input("\nPlease enter the playlist URL: ").strip()
    resolution = input("\nPlease choose resolution (360p or 720p): ").strip().lower()

    if resolution not in ["360p", "720p"]:
        print("Invalid resolution. Please choose either 360p or 720p.")
        return

    playlist_id = get_playlist_id(playlist_url)
    if not playlist_id:
        return

    video_links = get_video_links(playlist_id)
    if not video_links:
        print("No videos found in the playlist.")
        return

    print(f"\nDownloading {len(video_links)} videos...")

    save_folder = os.path.join(os.getcwd(), playlist_id[:7])
    download_videos(video_links, resolution, save_folder)

    print("\nDownloading finished.")
    print(f"All videos are saved at: {save_folder}")

    # Open the directory in File Explorer
    subprocess.Popen(f'explorer {save_folder}')


if __name__ == "__main__":
    main()
