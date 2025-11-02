# tts_service.py
import uuid
import edge_tts

class TextToSpeechService:
    def __init__(self):
        self.voice = "en-US-JennyNeural"  # Change voice if needed

    async def synthesize(self, text: str) -> str:
        filename = f"response_{uuid.uuid4()}.mp3"
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(filename)
        return filename
