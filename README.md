# はじめに
dockerでpython(FastAPI)の環境構築の練習。
動画ファイルをアップロードして
動画情報を音声ファイルへ変換
  →音声データからWhisper-APIを使って文字起こし
  →文字起こしした内容をGPTへRequestし
要約して返却するAPIを作成しました。
(Pythonを触った事ない状態でチュートリアルだけ実践してから実装したものなのでご容赦ください。)


# 環境構築
①git clone https://github.com/CreareWorks/Transcription-proto.git

②cd {rootディレクトリ}

③docker-compose up -d
  (ここで依存関係にあるパッケージをインストールするように設定済)
  
④http://localhost:8080/docs にアクセス
　swaggerUIが表示されれば環境構築完了

# 文字起こし手順
①動画ファイルのアップロード
　- 動画ファイルをchunkしつつwavへ変換し一時フォルダへ保存
  - 一時保存したファイルパスをresponseします。
curl -X 'POST' \
  'http://localhost:8080/audio/save' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@short_test.mp4;type=video/mp4'

②文字起こし
  - ①のresponse内容を含めてAPI呼び出し
  - 文字起こし結果をresponse
curl -X 'POST' \
  'http://localhost:8080/audio/transacription' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "chunk_files": [
      XXX.wav",
      "XXX.wav"
    ],
    "file_path": "xxx.mp4",
    "audio_file_path": "XXX.wav"
  }'
