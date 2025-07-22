# she_music

## 项目依赖

1. python 通过 `pip install PyYAML mutagen Pillow yt-dlp` 安装依赖包, 并且通过下面方式添加路径:
    ```bash
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```
2. 需要安装 ffmpeg

## 下载方式1
通过 ./batch_download.sh 下载 playlist 中的所有音乐


## 下载方式2

### 添加歌曲下载流程
1. 首先添加歌手的歌曲信息, 通过 yaml 文件进行添加和整理;
2. 对于添加的歌手信息, 在 album_cover 中建立歌手目录, 然后将添加的专辑照片以 .jpg 的方式保存; 然后添加一张文件名为 歌手.jpg 的图片来处理单曲;
3. 将要下载的歌手歌曲信息的 yml 文件放在 library 目录下
4. 在 she_music 目录下通过`python3 download_from_library.py`进行歌曲的下载

### 具体做了什么?

download_from_library.py 具体做了什么?

1. 首先程序会从 library 中获取所有的 yml 文件;
2. 然后从逐个遍历 yml 文件, 从 yml 中获取所有歌曲信息;
3. 接下来会通过 youtube 搜索, 下载对应视频的音频并且保存到 download 目录下;
4. 接下来会重新设置音频文件的元数据信息, 包含但不仅限于艺术家, 专辑名, 歌曲标题, 年份, 专辑封面以及歌词;
