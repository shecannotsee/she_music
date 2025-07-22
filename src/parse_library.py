import os
import yaml

def parse_library(library_path):
    music_info = []

    for filename in os.listdir(library_path):
        if not filename.endswith(".yml"):
            continue

        filepath = os.path.join(library_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        artist = os.path.splitext(filename)[0]

        for album_name, album_data in data.items():
            year = album_data.get("year", None)
            songs = album_data.get("songs", [])

            for song in songs:
                # 处理既支持 title 字典格式，也支持直接字符串格式
                if isinstance(song, dict):
                    title = song.get("title", "")
                    song_year = song.get("year", year)
                else:
                    title = song
                    song_year = year

                music_info.append({
                    "artist": artist,
                    "album": album_name,
                    "year": song_year,
                    "title": title
                })

    return music_info

if __name__ == "__main__":
    print("RUN test...")
    music_info = parse_library("./library")
    for item in music_info:
        # item 是 dict
        artist = item["artist"]
        album = item["album"]
        year = item["year"]
        title = item["title"]
        print(f"{artist}-{title}-{album}-{year}")
