from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import traceback
from .general_utils import ask_gpt_prompt
from pydantic import BaseModel
from ..llm.ai_services import gpt4

router = APIRouter()
    
class StreamRequest(BaseModel):
    """Request body for streaming."""
    question: str

@router.post("/qna_general")
async def stream(body: StreamRequest):
    try:
        question = body.question
        inputs = {
            'question': question,
        }
        return StreamingResponse(
            gpt4.async_generate_stream(
                prompt=ask_gpt_prompt,
                input_=inputs
            ), 
            media_type="text/event-stream"
        )
    except Exception as e:
        traceback.print_exc()
        