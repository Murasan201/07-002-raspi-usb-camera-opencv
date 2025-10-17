# raspi-usb-camera-opencv

Raspberry Pi上でUSBカメラ（Logitech C270n）を利用し、PythonおよびOpenCVを用いて**静止画撮影**および**動画録画**を行う実用的なサンプルプログラムです。

## 概要

書籍読者が「カメラ認識 → プレビュー → 撮影 → 保存」までを再現できることを重視して設計されています。

## 必要なもの

### ハードウェア
- Raspberry Pi 5 / 4B（USB 2.0ポート）
- USBカメラ（Logitech C270n 推奨、他のUVC対応カメラも可）
- HDMIディスプレイ

### ソフトウェア
- Raspberry Pi OS (Bookworm以降、64bit)
- Python 3.11以上
- OpenCV (`opencv-python`)
- NumPy

## セットアップ

### 1. 必要なパッケージのインストール

```bash
sudo apt update
sudo apt install python3-opencv python3-numpy -y
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/Murasan201/07-002-raspi-usb-camera-opencv.git
cd 07-002-raspi-usb-camera-opencv
```

### 3. カメラの接続確認

USBカメラをRaspberry PiのUSBポートに接続し、以下のコマンドで認識されているか確認します。

```bash
lsusb
```

Logitech C270nの場合、以下のような出力が表示されます：
```
Bus 001 Device 002: ID 046d:0825 Logitech, Inc. Webcam C270
```

次に、カメラデバイスの割り当てを確認します：

```bash
v4l2-ctl --list-devices
```

## 使い方

### 静止画撮影（usb_photo_capture.py）

リアルタイム映像を表示し、スペースキーで静止画を撮影します。

```bash
python3 usb_photo_capture.py
```

**操作方法：**
- **スペースキー**: 静止画を撮影し、`usb_photo.jpg` として保存
- **qキー**: プログラムを終了

### 動画録画（usb_video_capture.py）

リアルタイム映像を表示し、録画の開始/停止をコントロールします。

```bash
python3 usb_video_capture.py
```

**操作方法：**
- **rキー**: 録画開始/停止（トグル）
- **qキー**: プログラムを終了

録画中は画面に「Recording...」と赤文字で表示され、`usb_video.avi` として保存されます。

## カメラインデックス（camera_index）について

### カメラインデックスの割り当て

Raspberry PiでOpenCVを使用する際、カメラは `/dev/videoX` というデバイスファイルとして認識されます。この `X` の番号がカメラインデックスに対応します。

#### Raspberry Pi 5の場合

Raspberry Pi 5では、ビデオデバイスは以下のように割り当てられています：

| デバイス | 用途 |
|---------|------|
| `/dev/video0` ～ `/dev/video7` | CSI（Camera Serial Interface）カメラ用 |
| `/dev/video8` ～ | **USBカメラ用** |
| `/dev/video19` | ハードウェアデコーダー |
| `/dev/video20` ～ `/dev/video35` | 画像処理パイプライン（pisp_be） |

そのため、本プログラムでは `camera_index = 8` を使用しています。

#### Raspberry Pi 4以前の場合

Raspberry Pi 4以前では、USBカメラは通常 `/dev/video0` に割り当てられます。この場合は、プログラム内の `camera_index = 8` を `camera_index = 0` に変更してください。

### カメラインデックスの確認方法

接続されているカメラとそのデバイス番号を確認するには、以下のコマンドを実行します：

```bash
v4l2-ctl --list-devices
```

出力例：
```
UVC Camera (046d:0825) (usb-xhci-hcd.0-1):
        /dev/video8
        /dev/video9
        /dev/media4
```

この例では、USBカメラは `/dev/video8` に割り当てられているため、`camera_index = 8` を使用します。

### 複数のUSBカメラを使用する場合

複数のUSBカメラを接続している場合、接続順に番号が割り当てられます：
- 1台目のUSBカメラ: `/dev/video8`
- 2台目のUSBカメラ: `/dev/video10` または `/dev/video11`

使用したいカメラのデバイス番号に合わせて `camera_index` を変更してください。

### プログラムでのカメラインデックス変更方法

プログラム内の以下の行を編集します：

```python
# USBカメラを初期化（Raspberry Pi 5ではUSBカメラは通常video8）
camera_index = 8  # ← この数値を変更
cap = cv2.VideoCapture(camera_index)
```

## トラブルシューティング

### カメラが認識されない

**症状：** 「エラー: カメラを開くことができませんでした」と表示される

**解決策：**

1. USBカメラが正しく接続されているか確認
   ```bash
   lsusb
   ```

2. ビデオデバイスが存在するか確認
   ```bash
   ls -l /dev/video*
   ```

3. カメラのデバイス番号を確認し、プログラム内の `camera_index` を修正
   ```bash
   v4l2-ctl --list-devices
   ```

### カメラのLEDが点灯しない

**症状：** プログラムを実行してもカメラのLEDが点灯しない

**原因：** カメラインデックスが間違っている可能性があります。

**解決策：** 上記の「カメラインデックスの確認方法」に従って、正しいデバイス番号を確認してください。

### 文字化けが発生する

**症状：** ターミナルで日本語が文字化けする

**解決策：** プログラムには既にUTF-8のエンコーディング宣言が含まれています。ターミナルのロケール設定を確認してください：

```bash
echo $LANG
```

`ja_JP.UTF-8` または `en_US.UTF-8` などが設定されていることを確認してください。

### フレームが取得できない

**症状：** 「エラー: フレームを取得できませんでした」と表示される

**解決策：**

1. カメラが他のプロセスで使用されていないか確認
   ```bash
   lsof /dev/video8
   ```

2. カメラの権限を確認
   ```bash
   groups
   ```
   `video` グループに所属していることを確認してください。

## ファイル構成

```
raspi-usb-camera-opencv/
├── usb_photo_capture.py          # 静止画撮影プログラム
├── usb_video_capture.py          # 動画録画プログラム
├── README.md                     # このファイル
├── CLAUDE.md                     # プロジェクトルールファイル
├── LICENSE                       # MITライセンス
└── raspi-usb-camera-opencv-requirements.md  # 要件定義書
```

## ライセンス

MIT License

© 2025 Murasan Lab

書籍読者および教育目的での再利用を許可します。

## 参考情報

- [OpenCV公式ドキュメント](https://docs.opencv.org/)
- [Raspberry Pi公式ドキュメント](https://www.raspberrypi.com/documentation/)
- [Video4Linux2 (V4L2) ドキュメント](https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/v4l2.html)
