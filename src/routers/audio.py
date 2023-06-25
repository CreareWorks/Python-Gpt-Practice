import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.audioService import audioService
from config.config import BASE_API_RESPONSE
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

# インスタンス生成
audio_service = audioService()

class FilePath(BaseModel):
    file_path: list

router = APIRouter()
@router.post("/audio/save", tags=["audio"])
async def save_audio(file: UploadFile = File(...)):
    try:
        # 動画保存→音声ファイルへ変換、分割
        result = await audio_service.save_audio(file)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=e
        )

@router.post("/audio/transacription", tags=["audio"])
async def transacription_audio(request: FilePath):
    try:
        # 文字起こし
        result = await audio_service.transacription_audio(request.file_path)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=e
        )