# Transcription-proto

# サーバ起動
uvicorn main:app --reload

# 文字起こし手順
①動画ファイルのアップロード
　- 動画ファイルをchunkしつつwavへ変換し一時フォルダへ保存
  - 一時保存したファイルパスをresponseします
curl -X 'POST' \
  'http://127.0.0.1:8000/audio/save' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@short_test.mp4;type=video/mp4'

②文字起こし
  - ①のresponse内容を含めてAPI呼び出し
  - 文字起こし結果をresponse
curl -X 'POST' \
  'http://127.0.0.1:8000/audio/transacription' \
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
