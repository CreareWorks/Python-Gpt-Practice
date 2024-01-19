import os, io
from fastapi import APIRouter, HTTPException, Request
from services.gptService import gptService
from config.config import BASE_API_RESPONSE

router = APIRouter()

@router.post("/gpt/merge")
async def merge_chunk_file_text(request: Request):
    # インスタンス生成
    gpt_service = gptService(os.getenv("OPEN_AI_API_KEY"))
    
    audio_data = await request.body()
    # 文字起こし
    return gpt_service.transcribe_speech(audio_data)


# プロンプト生成
@router.post("/gpt/transacription")
async def create_transacription(request: Request):
    try:
        transacript = await request.body()
        #文字起こし結果と定義済みのプロンプトから議事録を生成
        result = gpt_service.generate_minutes(transacript)
        
        return {
            "status_code": BASE_API_RESPONSE['REQUEST_SUCCESS'],
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=BASE_API_RESPONSE['BAD_REQUEST'],
            detail=str(e)
        )
        
    # 呼び出しサンプル
    # 統合した文字列をプロンプト共にchatGPTにRequest
     url = "http://127.0.0.1:8000/gpt/transacription"
     headers = {"Content-Type": "text/plain"}
     async with httpx.AsyncClient() as client:
         result = await client.post(url, headers=headers, data=concat_text) #ここに結合した文字列を投げる



