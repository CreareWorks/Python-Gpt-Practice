import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from services.audioService import audioService
from services.baseResponseServise import apiResponseServide
from config.config import BASE_API_RESPONSE
from pydantic import BaseModel

# インスタンス生成
audio_service: audioService = audioService()
api_response_servise: apiResponseServide = apiResponseServide()

class Request(BaseModel):
    chunk_files: list
    file_path: str
    audio_file_path: str

router: APIRouter = APIRouter()

@router.post("/audio/save", tags=["audio"])
async def save_audio(file: UploadFile = File(...)) -> dict:
    try:
        # 動画保存→音声ファイルへ変換、分割
        result: dict = await audio_service.save_audio(file)

        return api_response_servise.success_response(result)

    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=e
        )

@router.post("/audio/transacription", tags=["audio"])
async def transacription_audio(request: Request) -> dict:
    try:
        # 文字起こし
        result: str = await audio_service.transacription_audio(
            request.chunk_files,
            request.file_path,
            request.audio_file_path
        )

        return api_response_servise.success_response(result)

    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=e
        )