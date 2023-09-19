from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import traceback
from .cve_to_attack_utils import make_cve_to_attack_prompt
from pydantic import BaseModel
from ..llm.ai_services import gpt4

router = APIRouter()
    
class StreamRequest(BaseModel):
    """Request body for streaming."""
    query: str

@router.post("/cve_to_attack_stream")
async def stream(body: StreamRequest):
    try:
        query = body.query
        inputs = {
            'query': query,
        }
        prompt = make_cve_to_attack_prompt(query)
        return StreamingResponse(
            gpt4.async_generate_stream(
                prompt=prompt,
                input_=inputs
            ), 
            media_type="text/event-stream"
        )
    except Exception as e:
        traceback.print_exc()
        