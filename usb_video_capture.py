#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os

# USBカメラを初期化（Raspberry Pi 5ではUSBカメラは通常video8）
camera_index = 8
cap = cv2.VideoCapture(camera_index)

# カメラが正常に開かれたかを確認
if not cap.isOpened():
    print("エラー: カメラを開くことができませんでした")
    exit()

# 動画の設定を取得
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# FPSが0の場合はデフォルト値を設定
if fps == 0:
    fps = 20

print(f"カメラ解像度: {frame_width}x{frame_height}, FPS: {fps}")

# 動画エンコーダーの設定
fourcc = cv2.VideoWriter_fourcc(*'XVID')
save_path = os.path.abspath("usb_video.avi")
out = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

print("動画録画を開始します")
print("rキーで録画開始/停止、qキーで終了")
print("※プレビューウィンドウをクリックしてフォーカスを合わせてください")
print(f"保存先: {save_path}")

recording = False

while True:
    # フレームを読み取り
    ret, frame = cap.read()

    if not ret:
        print("エラー: フレームを取得できませんでした")
        break

    # 録画中の場合は録画状態を表示
    if recording:
        cv2.putText(frame, "Recording...", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        out.write(frame)

    # プレビュー画面を表示
    cv2.imshow('USB Camera Recording', frame)

    # キー入力を待機
    key = cv2.waitKey(1) & 0xFF

    # rキーで録画開始/停止
    if key == ord('r'):
        recording = not recording
        if recording:
            print("✓ 録画開始")
        else:
            print("✓ 録画停止")

    # qキーで終了
    elif key == ord('q'):
        break

# リソースを解放
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"✓ 動画が保存されました: {save_path}")
