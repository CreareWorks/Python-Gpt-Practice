import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.audioService import audioService
from config.config import BASE_API_RESPONSE
from dotenv import load_dotenv
load_dotenv()

# インスタンス生成
audio_service = audioService()

router = APIRouter()
@router.post("/audio/transacription", tags=["audio"])
async def transacription_audio(file: UploadFile = File(...)):
    try:
        # 音声ファイルへの変換および文字起こし文字列を返却
        result = await audio_service.transacription_audio(file)
        
        return result.json()

    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=str(e)
        )