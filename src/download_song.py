import os
import subprocess
import sys

def download_song(keyword: str, out_dir: str, output_name: str) -> bool:
    os.makedirs(out_dir, exist_ok=True)

    command = [
        "yt-dlp",
        f"ytsearch1:{keyword}",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", os.path.join(out_dir, output_name),
    ]

    result = subprocess.run(command)
    return result.returncode == 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 download_song.py <搜索关键词> <输出目录> <输出名称>")
        print("示例: python3 download_song.py '周杰伦 七里香' download 七里香.mp3")
        sys.exit(1)

    keyword = sys.argv[1]
    out_dir = sys.argv[2]
    output_name = sys.argv[3]

    success = download_song(keyword, out_dir, output_name)
    if success:
        print(f"✅ 成功下载: {keyword}")
    else:
        print(f"❌ 下载失败: {keyword}")
