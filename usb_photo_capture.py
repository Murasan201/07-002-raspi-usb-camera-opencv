#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# USBカメラを初期化（Raspberry Pi 5ではUSBカメラは通常video8）
camera_index = 8
cap = cv2.VideoCapture(camera_index)

# カメラが正常に開かれたかを確認
if not cap.isOpened():
    print("エラー: カメラを開くことができませんでした")
    exit()

print("カメラが正常に接続されました")
print("スペースキーを押して写真を撮影、qキーで終了")

while True:
    # フレームを読み取り
    ret, frame = cap.read()

    if not ret:
        print("エラー: フレームを取得できませんでした")
        break

    # プレビュー画面を表示
    cv2.imshow('USB Camera Preview', frame)

    # キー入力を待機
    key = cv2.waitKey(1) & 0xFF

    # スペースキーで撮影
    if key == ord(' '):
        cv2.imwrite("usb_photo.jpg", frame)
        print("写真 'usb_photo.jpg' が保存されました")

    # qキーで終了
    elif key == ord('q'):
        break

# カメラとウィンドウを解放
cap.release()
cv2.destroyAllWindows()
