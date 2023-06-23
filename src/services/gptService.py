import openai
from api.gptClient import gptClient
from config.config import GPT_FIRST_COMPLETE

class gptService:
    def __init__(self, OPEN_AI_API_KEY: str) -> None:
        self.gpt_client: gptClient = gptClient()  # インスタンス生成
        self.gpt_client.setOpenAiKey(OPEN_AI_API_KEY)  # OpenAiのAPI_KEYをセット
    
    # 音声ファイルをwhisperAPIに投入
    def transcribe_speech(self, audio):
        return self.gpt_client.getWhisperData(audio)
    
    # プロンプトをchatGPTにRequest
    def generate_minutes(self, transcript: str) -> str:
        system_template = """会議の文字起こし文字列を渡します。

        この会議のサマリーをMarkdown形式で作成してください。サマリーは、下記形式で書いてください。

        - 会議の目的
        - 会議の内容
        - 会議の結論"""

        completion = self.gpt_client.generateChatCompletion(system_template, transcript)
        
        return completion.choices[GPT_FIRST_COMPLETE].message.content