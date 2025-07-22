import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error, TDRC
from mutagen.mp3 import MP3
from PIL import Image

def _get_mime_type(image_path):
    try:
        with Image.open(image_path) as img:
            mime = Image.MIME.get(img.format)
            return mime
    except Exception as e:
        print(f"❌ 图片格式检测失败: {e}")
        return None

def set_metadata(mp3_file: str, title: str, artist: str, album: str, year: str, cover_path: str = None):
    if not os.path.exists(mp3_file):
        print(f"❌ MP3文件不存在: {mp3_file}")
        return

    print(f"封面路径: {cover_path}")

    # 设置基础元数据
    try:
        try:
            audio = EasyID3(mp3_file)
        except Exception as e:
            print(f"⚠️ EasyID3读取失败，尝试添加ID3标签: {e}")
            audio = MP3(mp3_file, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()
            audio.save()
            audio = EasyID3(mp3_file)

        audio["title"] = title
        audio["artist"] = artist
        audio["album"] = album
        audio["date"] = year
        audio.save(mp3_file)
        # ✅ 添加底层年份标签 TDRC（Doppler 需要这个）
        try:
            id3 = ID3(mp3_file)
            id3.delall("TDRC")  # 清除已有的年份字段，避免重复
            id3.add(TDRC(encoding=3, text=year))
            id3.save(mp3_file, v2_version=3)  # ✅ 强制保存为 ID3v2.3，Doppler 更兼容
        except Exception as e:
            print(f"⚠️ 设置底层年份标签失败: {e}")
        print(f"✅ 基础元数据已设置: {os.path.basename(mp3_file)}")
    except Exception as e:
        print(f"❌ 设置基础元数据失败: {e}")
        return

    # 添加封面
    if cover_path:
        if not os.path.exists(cover_path):
            print(f"❌ 封面图片文件不存在: {cover_path}")
            return

        mime = _get_mime_type(cover_path)
        if not mime:
            print(f"⚠️ 不支持或无法识别的封面图片格式，封面未添加")
            return

        try:
            mp3 = MP3(mp3_file, ID3=ID3)
        except Exception as e:
            print(f"❌ 读取MP3文件失败: {e}")
            return

        if mp3.tags is None:
            try:
                mp3.add_tags()
            except error as e:
                print(f"⚠️ 添加ID3标签失败（可能已有标签）: {e}")

        try:
            with open(cover_path, 'rb') as img:
                img_data = img.read()
            mp3.tags.add(
                APIC(
                    encoding=3,  # UTF-8
                    mime=mime,
                    type=3,  # front cover
                    desc='Cover',
                    data=img_data
                )
            )
            mp3.save(v2_version=3)
            print(f"✅ 已成功添加封面: {os.path.basename(cover_path)}")
        except Exception as e:
            print(f"❌ 添加封面失败: {e}")
            return

    else:
        print("⚠️ 未提供封面路径，跳过封面添加。")


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("用法: python3 set_metadata.py <mp3路径文件> <歌名> <歌手> <专辑> <年份> <专辑封面路径>")
        print("示例: python3 set_metadata.py ./downloads/七里香.mp3 七里香 周杰伦 七里香 2019 ./album_cover/周杰伦/七里香.jpg")
        sys.exit(1)

    mp3_file = sys.argv[1]
    title = sys.argv[2]
    artist = sys.argv[3]
    album = sys.argv[4]
    year = sys.argv[5]
    cover_path = sys.argv[6]

    set_metadata(mp3_file, title, artist, album, year, cover_path)
