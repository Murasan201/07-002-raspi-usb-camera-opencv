# トラブルシューティング

このドキュメントでは、USBカメラプログラムの使用中に発生した実際の問題とその解決方法を記録しています。

---

## 目次

1. [文字化け問題](#1-文字化け問題)
2. [カメラデバイスインデックスの問題](#2-カメラデバイスインデックスの問題)
3. [パーミッションエラー](#3-パーミッションエラー)

---

## 1. 文字化け問題

### 症状

プログラムを実行すると、日本語のメッセージが文字化けして表示される。

```
pi@raspberrypi:~/work/project/07-002-raspi-usb-camera-opencv $ python usb_photo_capture.py 
繧ｫ繝｡繝ｩ縺梧ｭ｣蟶ｸ縺ｫ謗･邯壹＆繧後∪縺励◆
繧ｹ繝壹・繧ｹ繧ｭ繝ｼ繧呈款縺励※蜀咏悄繧呈聴蠖ｱ縲〈繧ｭ繝ｼ縺ｧ邨ゆｺ・
```

### 原因

Pythonファイルにエンコーディング宣言が含まれていなかったため、日本語のコメントやprint文が正しく処理されなかった。

### 解決策

Pythonファイルの先頭に以下を追加：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

**実施内容：**
- `usb_photo_capture.py` にUTF-8エンコーディング宣言を追加
- `usb_video_capture.py` にUTF-8エンコーディング宣言を追加
- shebang行（`#!/usr/bin/env python3`）も追加して実行権限を明確化

**確認方法：**

```bash
head -3 usb_photo_capture.py
```

正しく修正されていれば以下のように表示されます：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

```

---

## 2. カメラデバイスインデックスの問題

### 症状

プログラムを実行すると以下のエラーが表示される：

```
カメラが正常に接続されました
スペースキーを押して写真を撮影、qキーで終了
エラー: フレームを取得できませんでした
```

また、カメラのLEDが全く点灯しない。

### 調査手順

#### 1. USBデバイスとしての認識確認

```bash
lsusb
```

**結果：**
```
Bus 001 Device 002: ID 046d:0825 Logitech, Inc. Webcam C270
```

✓ USBデバイスとして正しく認識されている

#### 2. ビデオデバイスファイルの確認

```bash
ls -l /dev/video*
```

**結果：**
多数の `/dev/video*` デバイスが存在することを確認

#### 3. カメラの割り当て確認（重要）

```bash
v4l2-ctl --list-devices
```

**結果：**
```
pispbe (platform:1000880000.pisp_be):
	/dev/video20 ～ /dev/video35
	...

rp1-cfe (platform:1f00110000.csi):
	/dev/video0 ～ /dev/video7
	...

UVC Camera (046d:0825) (usb-xhci-hcd.0-1):
	/dev/video8
	/dev/video9
	/dev/media4
```

✓ USBカメラは `/dev/video8` に割り当てられていることが判明

#### 4. ユーザーの権限確認

```bash
groups
```

**結果：**
```
pi adm dialout cdrom sudo audio video plugdev games users input render netdev lpadmin gpio i2c spi
```

✓ `video` グループに所属しており、権限は問題なし

### 原因

**Raspberry Pi 5では、ビデオデバイスの割り当てが以下のようになっている：**

| デバイス範囲 | 用途 |
|-------------|------|
| `/dev/video0` ～ `/dev/video7` | CSI（Camera Serial Interface）カメラ用 |
| `/dev/video8` ～ | **USBカメラ用** |
| `/dev/video19` | ハードウェアデコーダー |
| `/dev/video20` ～ `/dev/video35` | 画像処理パイプライン |

プログラムでは `camera_index = 0` (つまり `/dev/video0`) を使用していたが、実際のUSBカメラは `/dev/video8` に割り当てられていたため、フレームを取得できなかった。

**注意:** Raspberry Pi 4以前では、USBカメラは通常 `/dev/video0` に割り当てられるため、この問題は発生しない。

### 解決策

プログラム内の `camera_index` を 8 に変更：

```python
# 変更前
camera_index = 0

# 変更後
camera_index = 8  # Raspberry Pi 5ではUSBカメラは通常video8
```

**実施内容：**
- `usb_photo_capture.py` の `camera_index` を 0 から 8 に変更
- `usb_video_capture.py` の `camera_index` を 0 から 8 に変更
- コメントに Raspberry Pi 5 での動作を明記

**確認方法：**

プログラムを実行してカメラのLEDが点灯し、プレビュー画面が表示されることを確認。

### 他の環境での対応方法

自分の環境でどのデバイスにカメラが割り当てられているか確認するには：

```bash
v4l2-ctl --list-devices
```

出力から "UVC Camera" または使用しているカメラ名を探し、その下に表示されているデバイス番号（通常は最初の番号）を使用する。

---

## 3. パーミッションエラー

### 症状

プログラムでスペースキーを押しても画像が保存されない。

プログラムに保存エラーハンドリングを追加した後、以下のようなメッセージが表示される：

```
✗ エラー: 写真の保存に失敗しました
```

### 調査手順

#### 1. ディレクトリの権限確認

```bash
ls -la /home/pi/work/project/07-002-raspi-usb-camera-opencv/
```

**結果：**
```
drwxr-xr-x 3 root root 4096 10月 17 20:42 .
drwxr-xr-x 7 root root 4096 10月 17 18:35 ..
drwxr-xr-x 8 root root 4096 10月 17 20:54 .git
-rw-r--r-- 1 root root  245 10月 17 18:42 CLAUDE.md
-rw-r--r-- 1 root root 1064 10月 17 18:35 LICENSE
-rw-r--r-- 1 root root 6963 10月 17 20:42 README.md
...
```

**問題発見:** すべてのファイルとディレクトリの所有者が `root:root` になっている

#### 2. 現在のユーザー確認

```bash
whoami
```

**結果：**
```
pi
```

### 原因

プロジェクトのセットアップ時に `sudo` を使用してファイルを作成・編集したため、すべてのファイルとディレクトリの所有者が `root` になっていた。

`pi` ユーザーでプログラムを実行した際、このディレクトリに書き込み権限がないため、画像ファイルを保存できなかった。

### 解決策

ディレクトリとすべてのファイルの所有者を `pi` ユーザーに変更：

```bash
sudo chown -R pi:pi /home/pi/work/project/07-002-raspi-usb-camera-opencv
```

**オプション説明：**
- `-R`: 再帰的に、ディレクトリ内のすべてのファイルとサブディレクトリも変更
- `pi:pi`: 所有者を `pi` ユーザー、グループを `pi` に設定

**確認方法：**

```bash
ls -la /home/pi/work/project/07-002-raspi-usb-camera-opencv/
```

すべてのファイルとディレクトリが `pi pi` と表示されることを確認：

```
drwxr-xr-x 3 pi   pi   4096 10月 17 20:42 .
drwxr-xr-x 7 root root 4096 10月 17 18:35 ..
drwxr-xr-x 8 pi   pi   4096 10月 17 20:54 .git
-rw-r--r-- 1 pi   pi    245 10月 17 18:42 CLAUDE.md
...
```

**書き込みテスト：**

```bash
touch test_write.txt && ls -l test_write.txt && rm test_write.txt
```

ファイルが正常に作成・削除できることを確認。

### 予防策

今後、ファイルを作成・編集する際は：

1. **通常のユーザー権限で実行** - `sudo` を使わずにファイル操作を行う
2. **必要な場合のみsudoを使用** - システムファイルや特権が必要な操作のみ
3. **Gitの設定** - Gitリポジトリの操作も通常ユーザーで行う

もし誤って `sudo` でファイルを作成してしまった場合は、上記の `chown` コマンドで修正する。

---

## プログラムの改善履歴

上記の問題解決に加えて、ユーザビリティを向上させるために以下の改善を実施しました：

### 1. 保存先パスの明示

プログラム起動時に保存先の絶対パスを表示：

```python
import os

save_path = os.path.abspath("usb_photo.jpg")
print(f"保存先: {save_path}")
```

### 2. 保存成功/失敗の明確なフィードバック

```python
success = cv2.imwrite(save_path, frame)
if success:
    print(f"✓ 写真が保存されました: {save_path}")
else:
    print(f"✗ エラー: 写真の保存に失敗しました")
```

### 3. フォーカスに関する注意喚起

OpenCVウィンドウにフォーカスを合わせる必要があることをユーザーに通知：

```python
print("※プレビューウィンドウをクリックしてフォーカスを合わせてください")
```

---

## よくある質問（FAQ）

### Q1: プログラムを実行してもキー入力が反応しない

**A:** OpenCVのプレビューウィンドウをクリックして、フォーカスを合わせてください。ターミナルウィンドウにフォーカスがある状態ではキー入力が検知されません。

### Q2: 複数のUSBカメラがある場合はどうすればいいですか？

**A:** `v4l2-ctl --list-devices` で各カメラのデバイス番号を確認し、使用したいカメラのインデックスをプログラム内で指定してください。通常、接続順に番号が割り当てられます（例: `/dev/video8`, `/dev/video10` など）。

### Q3: Raspberry Pi 4で動作しますか？

**A:** はい、動作します。ただし、Raspberry Pi 4ではUSBカメラが `/dev/video0` に割り当てられる可能性が高いため、プログラム内の `camera_index = 8` を `camera_index = 0` に変更する必要があるかもしれません。`v4l2-ctl --list-devices` で確認してください。

### Q4: HDMIディスプレイなしでも使えますか？

**A:** プログラムはGUIウィンドウ（プレビュー）を表示するため、ディスプレイが必要です。ヘッドレス環境で使用する場合は、VNC接続を使用するか、プログラムを修正してGUI部分を削除する必要があります。

### Q5: カメラの解像度を変更できますか？

**A:** はい、可能です。以下のコードを `VideoCapture` の直後に追加してください：

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

---

## 参考コマンド一覧

### カメラ関連

```bash
# USBデバイス一覧
lsusb

# ビデオデバイスとカメラの対応を確認
v4l2-ctl --list-devices

# ビデオデバイスファイル一覧
ls -l /dev/video*

# カメラの詳細情報を取得
v4l2-ctl --device=/dev/video8 --all

# カメラがサポートする解像度を確認
v4l2-ctl --device=/dev/video8 --list-formats-ext
```

### 権限関連

```bash
# 現在のユーザーを確認
whoami

# 所属グループを確認
groups

# ファイル/ディレクトリの所有者と権限を確認
ls -la

# 所有者を変更（再帰的）
sudo chown -R pi:pi /path/to/directory

# 特定のデバイスを使用中のプロセスを確認
lsof /dev/video8
```

### ファイル関連

```bash
# ファイルの存在確認
ls -lh usb_photo.jpg

# ファイル検索
find /home/pi -name "usb_photo.jpg"

# ディレクトリ内のファイル一覧（詳細）
ls -lah
```

---

## 開発環境のセットアップチェックリスト

新しい環境でプロジェクトをセットアップする際のチェックリスト：

- [ ] USBカメラが物理的に接続されている
- [ ] `lsusb` でカメラが認識されている
- [ ] `v4l2-ctl --list-devices` でカメラのデバイス番号を確認
- [ ] プログラム内の `camera_index` が正しく設定されている
- [ ] 必要なパッケージがインストールされている（`python3-opencv`, `python3-numpy`）
- [ ] プロジェクトディレクトリの所有者が正しいユーザーになっている
- [ ] 現在のユーザーが `video` グループに所属している
- [ ] HDMIディスプレイが接続されている（GUIプレビュー用）
- [ ] ファイルのエンコーディング宣言が正しい（UTF-8）

---

## サポート

問題が解決しない場合は、以下の情報を含めてissueを作成してください：

1. 使用しているRaspberry Piのモデル（例: Raspberry Pi 5）
2. OSのバージョン（`cat /etc/os-release` の出力）
3. 使用しているカメラのモデル
4. `v4l2-ctl --list-devices` の出力
5. エラーメッセージの全文
6. 実行したコマンドと出力

リポジトリ: https://github.com/Murasan201/07-002-raspi-usb-camera-opencv
