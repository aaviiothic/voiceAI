import openai
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    async def transcribe_async(self, file_bytes: bytes, filename: str) -> str:
        """Transcribe audio using Whisper API"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            audio_file = open(tmp.name, "rb")
            transcript = openai.Audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcript.text.strip()

    async def text_to_speech_async(self, text: str, output_path: str):
        """Convert text to speech"""
        response = openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            response.stream_to_file(f)

    async def get_chat_response_async(self, session_msgs: list, context: str) -> str:
        """Get chat completion from GPT"""
        messages = [{"role": "system", "content": f"Context: {context}"}]
        for msg in session_msgs:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return completion.choices[0].message.content.strip()
