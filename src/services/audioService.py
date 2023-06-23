import os, aiofiles, httpx, tempfile
from fastapi import FastAPI, UploadFile, File, Form
from pydub import AudioSegment
from pathlib import Path

class audioService:
    def __init__(self) -> None:
        pass
        
    async def transacription_audio(self, file: UploadFile = Form(...)):
        # 動画ファイルを一時的な保存先に保存
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 音声ファイルに変換
        audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", os.path.splitext(file.filename)[0] + ".wav")
        AudioSegment.from_file(file_path).export(audio_file, format="wav")
        
        # 音声ファイルの分割
        chunk_duration = 100  # 分割するチャンクの長さ（秒）10分
        audio = AudioSegment.from_file(audio_file)
        total_duration = len(audio)
        chunk_files = []
        start_time = 0
        end_time = chunk_duration * 1000
        while start_time < total_duration:
            if end_time > total_duration:
                end_time = total_duration
            chunk = audio[start_time:end_time]
            chunk_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", f"output{start_time//1000:03d}.wav")
            chunk.export(chunk_file, format="wav")
            chunk_files.append(chunk_file)
            start_time = end_time
            end_time += chunk_duration * 1000

        # 分割音声ファイルから文字起こし内容を統合(Post)
        url = "http://127.0.0.1:8000/gpt/merge"
        headers = {"Content-Type": "audio/wav"}
        responses = []
        async with httpx.AsyncClient() as client:
            for chunk_file in chunk_files:
                async with aiofiles.open(chunk_file, "rb") as audio_data:
                    response = await client.post(url, headers=headers, content=str(Path(audio_data.name)))
                    # ここでprintすると400
        print(response.json()) #これで受け取る

        #whisperAPIに渡す値
        # <_io.BufferedReader name='/Users/oshimayota/Documents/project_source/transcription-proto/src/services/output000.wav'>

        
        # 統合した文字列をプロンプト共にchatGPTにRequest
        #url = "http://127.0.0.1:8000/gpt/transacription"
        #headers = {"Content-Type": "audio/wav"}
        #result = await client.post(url, headers=headers, files={"transcript": ""}) #ここに結合した文字列を投げる

        # 一時ファイルの削除
        #os.remove(file_path)
        #os.remove(audio_file)
        #for chunk_file in chunk_files:
        #    os.remove(chunk_file)

        # 議事録結果を返却
        #return result
