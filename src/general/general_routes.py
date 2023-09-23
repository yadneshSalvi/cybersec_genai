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
async def qna(body: StreamRequest):
    """
    Args:
        question (str): user question for which we want to find answer
    Returns:
        Json with following fields
        query (str): the question sent to gpt
        response (str): the response from gpt
    """
    try:
        question = body.question
        inputs = {
            'question': question,
        }
        response = await gpt4.async_generate(
            prompt=ask_gpt_prompt,
            input_=inputs
        )
        return {
            "query": question,
            "response": response
        }
    except Exception as e:
        traceback.print_exc()

@router.post("/qna_general_stream")
async def qna_stream(body: StreamRequest):
    """
    Args:
        question (str): user question for which we want to find answer
    Returns:
        StreamingResponse: gpt explanation for user question
    """
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
        