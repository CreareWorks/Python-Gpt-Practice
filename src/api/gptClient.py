import openai
from typing import Dict

class gptClient:
    # openAi Apiキーをセット
    def setOpenAiKey(self, OPEN_AI_API_KEY: str) -> None:
        openai.api_key = OPEN_AI_API_KEY
    
    # whisperApiに音声データを渡し文字列を返却
    def getWhisperData(self, audio_file_path: str) -> str:
        with open(audio_file_path, "rb") as audio_file:
            result = openai.Audio.transcribe("whisper-1", audio_file)
            return result.text
    
    # chatGptに文字起こし内容と定義済みプロンプトを元に議事録生成依頼
    def generateChatCompletion(
            self,
            system_template: str,
            transcript: str
        ) -> Dict:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_template},
                {"role": "user", "content": transcript.decode('utf-8')}
            ]
        )
        return completion
