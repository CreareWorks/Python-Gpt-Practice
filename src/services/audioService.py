import os, aiofiles, httpx, tempfile
from fastapi import FastAPI, UploadFile, File, Form
from pydub import AudioSegment
from pathlib import Path
import requests

class audioService:
    def __init__(self) -> None:
        pass
        
    async def save_audio(self, file: UploadFile = Form(...)):
        # 動画ファイルを一時的な保存先に保存
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 音声ファイルに変換
        audio_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", os.path.splitext(file.filename)[0] + ".wav")
        AudioSegment.from_file(file_path).export(audio_file, format="wav")
        
        # 音声ファイルの分割
        chunk_duration = 60
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
        
        return chunk_files

    async def transacription_audio(self, chunk_files):
        # 分割音声ファイルから文字起こし内容を統合(Post)
        url = "http://127.0.0.1:8000/gpt/merge"
        headers = {"Content-Type": "audio/wav"}
        concat_text = ""
        async with httpx.AsyncClient(timeout=60) as client:
            for chunk_file in chunk_files:
                async with aiofiles.open(chunk_file, "rb") as audio_data:
                    response = await client.post(url, headers=headers, content=str(Path(audio_data.name)))
                    concat_text += response.read().decode('utf-8')
                    
        # 一時ファイルの削除
        #os.remove(file_path)
        #os.remove(audio_file)
        #for chunk_file in chunk_files:
        #    os.remove(chunk_file)
        
        return concat_text
