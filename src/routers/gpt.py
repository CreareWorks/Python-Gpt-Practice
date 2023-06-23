import os, io
from fastapi import APIRouter, HTTPException, Request
from services.gptService import gptService
from typing import Dict, Any, BinaryIO
from config.config import BASE_API_RESPONSE
from dotenv import load_dotenv
load_dotenv()


# インスタンス生成
gpt_service = gptService(os.getenv("OPEN_AI_API_KEY"))

router = APIRouter()

@router.post("/gpt/merge")
async def merge_chunk_file_text(request: Request):
    audio_data = await request.body()
    # 文字起こしと議事録生成
    return gpt_service.transcribe_speech(audio_data)

@router.post("/gpt/transacription")
async def create_transacription(transcript) -> Dict[str, Any]:
    try:
        #文字起こし結果と定義済みのプロンプトから議事録を生成
        result = gpt_service.generate_minutes(transcript)
        
        return {
            "status_code": BASE_API_RESPONSE['REQUEST_SUCCESS'],
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=str(e)
        )
        



# 残タスク　音声録音？　必要？
# <aiofiles.threadpool.binary.AsyncBufferedReader object at 0x103b6a220> wrapping <_io.BufferedReader name='/Users/oshimayota/Documents/project_source/transcription-proto/src/services/../../temp/output000.wav'>