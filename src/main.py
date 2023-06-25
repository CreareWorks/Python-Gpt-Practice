from fastapi import FastAPI, APIRouter, Request, status
from starlette.middleware.cors import CORSMiddleware 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import gpt
from routers import audio

# create アプリケーション本体のinstanceを生成
app = FastAPI(
    debug=True, #検証中
    multipart=True
    )

app.max_request_size = 50 * 1024 * 1024

# cors対策
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]   
)
# 422エラー詳細ハンドリング
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

# 各Routerを呼び出す為の定義
router = APIRouter()

# 文字起こし機能のrouter定義
app.include_router(gpt.router)
# 音声変換router定義
app.include_router(audio.router)