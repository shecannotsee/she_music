#!/bin/bash

KEYWORD="$1"
SUBFOLDER="${2:-default}"  # 如果没传就用 default 文件夹
OUTDIR="./downloads/$SUBFOLDER"

mkdir -p "$OUTDIR"

yt-dlp \
    "ytsearch1:$KEYWORD" \
    --extract-audio \
    --audio-format mp3 \
    --audio-quality 0 \
    -o "$OUTDIR/%(title)s.%(ext)s"

