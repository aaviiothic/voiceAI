from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse
import uuid
import os

from openai_service import OpenAIService
from milvus_service import MilvusDbService

router = APIRouter(prefix="/api/audio", tags=["Audio"])
openai_service = OpenAIService()
milvus_service = MilvusDbService()

sessions = {}

@router.post("/listen")
async def listen(
    file: UploadFile = File(...),
    sessionId: str = Query(...),
    collectionId: str = Query("my_collection")
):
    try:
        file_bytes = await file.read()

        user_text = await openai_service.transcribe_async(file_bytes, file.filename)

        if not user_text or len(user_text.strip()) < 2:
            silence_resp = "Sorry, I didn’t hear you. Are you there?"
            out_path = f"wwwroot/static/audio/{uuid.uuid4()}.mp3"
            await openai_service.text_to_speech_async(silence_resp, out_path)
            return {
                "userText": "",
                "botText": silence_resp,
                "audioUrl": f"/static/audio/{os.path.basename(out_path)}",
                "isSilence": True
            }

        if sessionId not in sessions:
            sessions[sessionId] = []

        sessions[sessionId].append({"user": user_text, "assistant": ""})

        context = await milvus_service.query_knowledge_async(user_text, collectionId)

        bot_text = await openai_service.get_chat_response_async(sessions[sessionId], context)
        sessions[sessionId][-1]["assistant"] = bot_text

        out_path = f"wwwroot/static/audio/{uuid.uuid4()}.mp3"
        await openai_service.text_to_speech_async(bot_text, out_path)

        return {
            "userText": user_text,
            "botText": bot_text,
            "audioUrl": f"/static/audio/{os.path.basename(out_path)}",
            "isSilence": False
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
