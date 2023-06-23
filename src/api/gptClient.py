import openai
from typing import BinaryIO,Dict

class gptClient:
    # openAi Apiキーをセット
    def setOpenAiKey(self, OPEN_AI_API_KEY:str) -> None:
        openai.api_key = OPEN_AI_API_KEY
    
    # whisperApiに音声データを渡し文字列を返却
    def getWhisperData(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            result = openai.Audio.transcribe("whisper-1", audio_file)
            return result.text
    
    # chatGptに文字起こし内容と定義済みプロンプトを元に議事録生成依頼
    def generateChatCompletion(
            self,
            system_template:str,
            transcript:Dict[str, str]
        ) -> str:
        return openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": system_template},
                {"role": "user", "content": transcript.text}
            ],
            # 出力する単語のランダム性（0から2の範囲 小数点含む) 0=返答内容固定
            temperature=0
        )