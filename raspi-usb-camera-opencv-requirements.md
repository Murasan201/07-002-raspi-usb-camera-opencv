# 📘 要件定義書  
**プロジェクト名:** raspi-usb-camera-opencv  
**作成者:** Murasan Lab  
**作成日:** 2025年10月17日  
**関連書籍章:** 「USBカメラを活用する」  

---

## 1. プロジェクト概要

本プロジェクトは、Raspberry Pi上でUSBカメラ（Logitech C270n）を利用し、  
PythonおよびOpenCVを用いて**静止画撮影**および**動画録画**を行う  
実用的なサンプルプログラムを提供することを目的とする。  

書籍読者が「カメラ認識 → プレビュー → 撮影 → 保存」までを  
再現できることを重視して設計されている。  

---

## 2. 目的とスコープ

### 目的
- 書籍内で紹介するUSBカメラプログラムの再現性を確保する。  
- OpenCVによる画像キャプチャの基本的な操作を理解させる。  
- Raspberry Pi環境におけるUVC（USB Video Class）対応カメラ制御の基礎を学習させる。  

### スコープ
- Raspberry Pi OS (64bit) 上で動作。  
- 対応デバイス：Logitech C270n（他のUVC対応カメラも可）。  
- 使用言語：Python 3.11 以上。  
- 外部ライブラリ：OpenCV（`opencv-python`）、NumPy。  

---

## 3. システム構成概要

| 要素 | 内容 |
|------|------|
| **ハードウェア** | Raspberry Pi 5 / 4B（USB 2.0ポート）<br>USBカメラ（Logitech C270n） |
| **OS** | Raspberry Pi OS (Bookworm以降、64bit) |
| **開発言語** | Python 3.x |
| **主要ライブラリ** | OpenCV (`opencv-python`), NumPy |
| **保存先** | ローカルディレクトリに静止画（jpg）・動画（avi）を保存 |
| **入出力デバイス** | USBカメラ映像入力 / HDMIディスプレイ出力 |

---

## 4. 機能要件

### 4.1 静止画撮影機能（`usb_photo_capture.py`）
- USBカメラからリアルタイム映像を取得。  
- プレビュー画面を表示。  
- **スペースキー押下**で静止画を撮影し、`usb_photo.jpg`として保存。  
- **qキー**でプログラムを終了。  
- カメラ未接続時にエラーメッセージを表示。

### 4.2 動画録画機能（`usb_video_capture.py`）
- USBカメラ映像を取得しプレビュー表示。  
- **rキー**で録画開始・停止をトグル制御。  
- **qキー**でプログラム終了。  
- 録画中は「Recording...」の文字を画面に重ねて表示。  
- 保存形式：`usb_video.avi`、コーデックはXVID。  

---

## 5. 非機能要件

| 項目 | 要件 |
|------|------|
| **実行速度** | プレビュー時 20fps以上を維持 |
| **互換性** | UVC対応カメラ全般で動作可能 |
| **可搬性** | Raspberry Pi 4B以降で動作確認済み |
| **保守性** | 各プログラムが独立して実行可能 |
| **再現性** | 書籍の手順通りに実行すれば同一結果が得られること |
| **エラーハンドリング** | カメラ未接続・ファイル保存失敗時にエラー出力 |

---

## 6. ディレクトリ構成

```
raspi-usb-camera-opencv/
├── usb_photo_capture.py          # 静止画撮影プログラム
├── usb_video_capture.py          # 動画録画プログラム
├── requirements.txt              # 使用ライブラリ一覧
├── README.md                     # 解説・使用方法
└── images/
    └── sample_capture.jpg        # サンプル画像
```

---

## 7. 実行環境セットアップ

```bash
sudo apt update
sudo apt install python3-opencv python3-numpy -y
git clone https://github.com/murasan-lab/raspi-usb-camera-opencv.git
cd raspi-usb-camera-opencv
python3 usb_photo_capture.py
```

---

## 8. テスト項目

| テスト項目 | 期待結果 |
|-------------|-----------|
| USBカメラが認識される | `lsusb`でLogitech C270nが表示される |
| `/dev/video0`が生成される | `v4l2-ctl --list-devices`で確認可能 |
| プレビューが表示される | OpenCVウィンドウが表示される |
| スペースキーで静止画保存 | `usb_photo.jpg`が作成される |
| 録画ファイルが作成される | `usb_video.avi`が再生可能 |
| 録画中に「Recording...」表示 | プレビュー画面上に赤文字で表示される |

---

## 9. ライセンス・著作権

- **ライセンス:** MIT License  
- **著作権:** © 2025 Murasan Lab  
- **使用許諾:** 書籍読者および教育目的での再利用を許可。  

---

## 10. リポジトリ説明文（英語）

> A practical Raspberry Pi project using a USB webcam (Logitech C270n) with Python and OpenCV.  
> Includes sample scripts for photo capture and video recording.  
> Ideal for beginners learning Raspberry Pi camera programming and computer vision basics.  
