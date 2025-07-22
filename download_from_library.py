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
DOWNLOAD_DIR = os.path.join(CURRENT_DIR, "download")
ALBUM_COVER_DIR = os.path.join(CURRENT_DIR, "album_cover")

# 1. 获取所有的音乐信息
all_music_info = parse_library(PARSE_DIR)

for item in all_music_info:
    artist = item["artist"] # 歌手
    title = item["title"]   # 歌名
    album = item["album"]   # 专辑名(如果是单曲则是:单曲+数字的形式, 例如单曲1)
    year = str(item["year"])     # 歌曲发布年份
    
    logging.info(f"当前歌曲信息如下:")
    logging.info(f"歌手: {artist};歌名: {title};专辑名: {album};年份: {year}")

    # 参数处理-------------------------------------------------------------------------------------------------------------
    # 查询下载的搜索关键字
    search_keywords: str = (f"{artist} {album} {title}" # 非单曲加入专辑搜索
                            if album[:2] != "单曲" else 
                            f"{artist} {title}") # 单曲查询不附带专辑信息
    # 设置音乐文件的专辑
    set_album: str = (album # 非单曲时直接使用专辑名
                      if album[:2] != "单曲" else
                      f"{artist}单曲") # 单曲的专辑名统一被称为: 某歌手单曲
    # 下载目录
    save_dir: str = os.path.join(DOWNLOAD_DIR, artist, set_album)
    # 下载保存下来的文件名
    save_file_name: str = f"{title}.mp3"
    # 设置下载文件路径
    save_file: str = os.path.join(save_dir, save_file_name) # 下载的文件路径
    # 设置音乐文件的标题
    set_title: str = title
    # 设置音乐文件的艺人
    set_artist: str = artist
    # 设置音乐文件的年份
    set_year: str = year
    # 保存时歌曲封面的图片路径
    set_album_cover_file: str = (f"{ALBUM_COVER_DIR}/{artist}/{album}.jpg" # 非单曲使用目录下的专辑图像来处理封面
                                 if album[:2] != "单曲" else 
                                 f"{ALBUM_COVER_DIR}/{artist}/歌手.jpg") # 单曲则使用目录下 歌手.jpg 来处理封面
    # 参数处理-------------------------------------------------------------------------------------------------------------

    # 2. 下载歌曲
    logging.info(f"查询关键字为: {search_keywords}")
    logging.info(f"歌曲的下载路径为: {save_file}")
    success = download_song(search_keywords, save_dir, save_file_name)
    # 3.检查下载是否成功
    if success:
        logging.info(f"✅ 成功下载: {search_keywords}")
    else:
        logging.error(f"❌ 下载失败: {search_keywords}")
        continue
    # 4. 为歌曲更新元数据
    logging.info(f"元数据设置信息如下({save_file}):")
    logging.info(f"歌名: {set_title}, 艺术家: {set_artist}, 所属专辑: {set_album}, 年份: {set_year}, 专辑封面路径: {set_album_cover_file}")
    set_metadata(save_file, set_title, set_artist, set_album, set_year, set_album_cover_file)

        


