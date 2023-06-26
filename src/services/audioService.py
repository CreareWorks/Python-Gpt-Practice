import os,aiofiles,httpx,uuid
from fastapi import UploadFile,Form
from pydub import AudioSegment
from pathlib import Path
from typing import List

class audioService:
    def __init__(self) -> None:
        pass
        
    async def save_audio(self, file: UploadFile = Form(...)) -> dict:
        # ユニーク識別させる為、uuid生成
        new_uuid: uuid.UUID = uuid.uuid4()
        
        # 動画ファイルを一時的な保存先に保存
        file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", str(new_uuid) + file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 音声ファイルに変換
        # HACK m4aで圧縮したいところ。 wavは重いのでmp3で対応(mp3に圧縮した時の音質低下が気になるところ。)
        audio_file: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", os.path.splitext(file.filename)[0] + str(new_uuid) + ".mp3")
        AudioSegment.from_file(file_path).export(audio_file, format="mp3")
        
        # 音声ファイルの分割
        chunk_duration: int = 60
        audio: AudioSegment = AudioSegment.from_file(audio_file)
        total_duration: int = len(audio)
        chunk_files: List[str] = []
        start_time: int = 0
        end_time: int = chunk_duration * 1000
        while start_time < total_duration:
            if end_time > total_duration:
                end_time = total_duration
            chunk: AudioSegment = audio[start_time:end_time]
            chunk_file: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../temp", f"output{start_time//1000:03d}" + str(new_uuid) + ".mp3")
            chunk.export(chunk_file, format="mp3")
            chunk_files.append(chunk_file)
            start_time = end_time
            end_time += chunk_duration * 1000
        
        return {
            "chunk_files" : chunk_files,
            "file_path" : file_path,
            "audio_file_path" : audio_file
        }

    async def transacription_audio(self, chunk_files: List[str], file_path: str, audio_file_path: str) -> str:
        # 分割音声ファイルから文字起こし内容を統合(Post)
        url: str = "http://127.0.0.1:8000/gpt/merge"
        headers: dict = {"Content-Type": "audio/wav"}
        concat_text: str = ""
        async with httpx.AsyncClient(timeout=60) as client:
            for chunk_file in chunk_files:
                async with aiofiles.open(chunk_file, "rb") as audio_data:
                    response = await client.post(url, headers=headers, content=str(Path(audio_data.name)))
                    concat_text += response.read().decode('utf-8')
                    
        # 一時ファイルの削除
        os.remove(file_path)
        os.remove(audio_file_path)
        for chunk_file in chunk_files:
            os.remove(chunk_file)
        
        return concat_text
