import os
import subprocess
import sys
import logging
from src.download_song import download_song
from src.parse_library import parse_library
from src.set_metadata import set_metadata
from src.path import check_current_dir_is

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 检查工作路径
WORK_DIR = "she_music"
if check_current_dir_is(WORK_DIR):
    print("处于目录 she_music")
else:
    print("不处于目录 she_music")
# 获取当前路径并设置一些路径
CURRENT_DIR = os.getcwd()
PARSE_DIR = os.path.join(CURRENT_DIR, "library")
SONGS_SAVE_PATH = os.path.join(CURRENT_DIR, "download")
ALBUM_COVER_PATH = os.path.join(CURRENT_DIR, "album_cover")

# 1. 获取所有的音乐信息
all_music_info = parse_library(PARSE_DIR)

for item in all_music_info:
    artist = item["artist"] # 歌手
    title = item["title"]   # 歌名
    album = item["album"]   # 专辑名(如果是单曲则是:单曲+数字的形式, 例如单曲1)
    year = item["year"]     # 歌曲发布年份
    
    logging.info(f"当前歌曲信息如下:")
    logging.info(f"歌手: {artist};歌名: {title};专辑名: {album};年份: {year}")

    # 参数处理-------------------------------------------------------------------------------------------------------------
    # 查询下载的搜索关键字
    search_keywords: str = (f"{artist} {album} {title}" if album[:2] != "单曲" else # 非单曲加入专辑搜索
                            f"{artist} {title}") # 单曲查询不附带专辑信息
    # 设置音乐文件的专辑
    set_album: str = (album if album[:2] != "单曲" else # 非单曲时直接使用专辑名
                      f"{artist}单曲")# 单曲的专辑名统一被称为: 某歌手单曲
    # 下载目录
    download_dir: str = os.path.join(SONGS_SAVE_PATH, artist,)
    # 下载保存下来的文件名
    download_file: str = f"{title}.mp3"

    download_file_path: str = os.path.join(download_dir, download_file) # 下载的文件路径
    # 设置音乐文件的标题
    set_title: str = title
    # 设置音乐文件的艺人
    set_artist: str = artist

    # 设置音乐文件的年份
    set_year: str = year
    # 保存时歌曲封面的图片路径
    set_album_cover_path: str = (f"{ALBUM_COVER_PATH}/{artist}/{album}.jpg" if album[:2] != "单曲" else # 使用目录下的专辑图像来处理封面
                                f"{ALBUM_COVER_PATH}/{artist}/歌手.jpg") # 使用目录下 歌手.jpg 来处理封面
    # 参数处理-------------------------------------------------------------------------------------------------------------

    # 2. 下载歌曲
    logging.info(f"查询关键字为: {search_keywords}")
    logging.info(f"歌曲的下载路径为: {SONGS_SAVE_PATH}/{title}.mp3")
    success = download_song(search_keywords, SONGS_SAVE_PATH, title)

    # 3.检查下载是否成功
    if success:
        logging.info(f"✅ 成功下载: {search_keywords}")
    else:
        logging.error(f"❌ 下载失败: {search_keywords}")
        continue


    # 4. 为歌曲更新元数据
    download_file_path = f"{SONGS_SAVE_PATH}/{title}.mp3" # 下载文件路径
    logging.info(f"元数据设置信息如下({download_file_path}):")
    logging.info(f"歌名: {title}, 艺术家: {artist}, 所属专辑: {set_album}, 年份: {year}, 专辑封面路径: {album_cover_path}")
    set_metadata(download_file_path, title, artist, set_album, year, album_cover_path)

        


