import os

def check_current_dir_is(dir_name: str) -> bool:
    """
    判断当前工作目录的最后一级目录名是否为指定的 dir_name。
    """
    current_dir = os.path.abspath(os.getcwd())
    last_dir = os.path.basename(current_dir)
    return last_dir == dir_name

if __name__ == "__main__":
    print("终端目录:", os.getcwd())
    print("脚本路径:", os.path.abspath(__file__))
    print("__file__: ", __file__)

    current_dir = os.path.abspath(os.getcwd())
    print(f"当前路径：{current_dir}")

    if check_current_dir_is("she_music"):
        print("处于目录 she_music")
    else:
        print("不处于目录 she_music")
