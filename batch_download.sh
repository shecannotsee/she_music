#!/bin/bash

DOWNLOAD_SCRIPT="./download.sh"
DOWNLOAD_ROOT="./downloads"
FAILED_LOG="failed.log"

# 清空之前的失败日志
> "$FAILED_LOG"

for txtfile in ./playlist/*.txt; do
    foldername="${txtfile%.txt}"   # 例如 1.txt -> 1
    outdir="$DOWNLOAD_ROOT/$foldername"
    mkdir -p "$outdir"

    echo "📖 正在处理文件: $txtfile"

    while IFS= read -r line || [ -n "$line" ]; do
        # 去除BOM和首尾空白
        keyword=$(echo "$line" | sed 's/^[ \t]*//;s/[ \t]*$//' | sed 's/^\xEF\xBB\xBF//')
        if [[ -z "$keyword" ]]; then
            continue
        fi

        # 生成安全的文件名，避免特殊字符
        safe_name=$(echo "$keyword" | sed 's/[\/:*?"<>|]/-/g')

        # 检查对应mp3文件是否已经存在
        if ls "$outdir/"*"$safe_name"*.mp3 1> /dev/null 2>&1; then
            echo "⚠️ 歌曲已存在，跳过下载: $keyword"
            continue
        fi

        echo "🎵 开始下载: $keyword"

        # 传入额外参数，告诉download.sh存到对应文件夹
        if bash "$DOWNLOAD_SCRIPT" "$keyword" "$foldername"; then
            echo "✅ 下载成功: $keyword"
        else
            echo "❌ 下载失败: $keyword"
            echo "$keyword" >> "$FAILED_LOG"
        fi

        echo "--------------------------------"

    done < "$txtfile"
done

echo "🎉 所有任务完成！"
echo "❗ 失败日志保存在 $FAILED_LOG"

