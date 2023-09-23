from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import traceback
from .cve_to_attack_utils import (
    make_cve_to_attack_prompt, get_json_from_text, 
    search_similar_cves, search_similar_cves_with_technique_descp
)
from pydantic import BaseModel
from ..llm.ai_services import gpt4
from .. import my_logger

router = APIRouter()
    
class StreamRequest(BaseModel):
    """Request body for streaming."""
    query: str

@router.post("/cve_to_attack_stream")
async def cve_to_attack_stream(body: StreamRequest):
    """
    Args:
        query (str): user query for which we want to find attack techniques
    Returns:
        StreamingResponse: gpt explanation and attack techniques
    """
    try:
        query = body.query
        prompt_template, prompt = make_cve_to_attack_prompt(query)
        inputs = {
            'prompt': prompt,
        }
        return StreamingResponse(
            gpt4.async_generate_stream(
                prompt=prompt_template,
                input_=inputs
            ), 
            media_type="text/event-stream"
        )
    except Exception as e:
        my_logger.error(f"Exception: {e}\n{traceback.format_exc()}")

@router.post("/cve_to_attack")
async def cve_to_attack(body: StreamRequest):
    """
    Args:
        query (str): user query for which we want to find attack techniques
    Returns:
        Json with following fields
        gpt_prompt (str): the prompt sent to gpt
        gpt_response (str): the response from gpt
        gpt_attack_prediction (object): the attack prediction from gpt
            contains field related_attacks which is a list of attacks
    """
    try:
        query = body.query
        prompt_template, prompt = make_cve_to_attack_prompt(query)
        inputs = {
            'prompt': prompt,
        }
        gpt_response = await gpt4.async_generate(
            prompt=prompt_template,
            input_=inputs
        )
        gpt_attack_prediction = get_json_from_text(
            gpt_response
        )
        return {
            "gpt_prompt": prompt,
            "gpt_response": gpt_response,
            "gpt_attack_prediction": gpt_attack_prediction
        }
    except Exception as e:
        my_logger.error(f"Exception: {e}\n{traceback.format_exc()}")
        return {
            "gpt_prompt": "",
            "gpt_response": "",
            "gpt_attack_prediction": {"related_attacks":[]}
        }
    
class SimilarCVEsRequest(BaseModel):
    """Request body for streaming."""
    query: str
    num_cves: int

@router.post("/similar_cves")
async def similar_cves(body: SimilarCVEsRequest):
    """
    Args:
        query (str): user query for which we want to find attack techniques
        num_cves (int): number of similar cves to return
    Returns:
        list of similar cves which contain objects with following fields
            cve_name(str), cve_description(str), attack_techniques(list)
    """
    try:
        query = body.query
        num_cves = body.num_cves
        similar_cves = search_similar_cves(query, num_cves)
        return similar_cves
    except Exception as e:
        my_logger.error(f"Exception: {e}\n{traceback.format_exc()}")
        return []
    
@router.post("/similar_cves_with_techniques_description")
async def similar_cves_with_technique_descp(
        body: SimilarCVEsRequest
    ):
    """
    Args:
        query (str): user query for which we want to find attack techniques
        num_cves (int): number of similar cves to return
    Returns:
        list of similar cves which contain objects with following fields
            cve_name(str), cve_description(str), 
            attack_techniques list of objects with following fields
                attack_technique_name(str)
                attack_technique_description(str)
    """
    try:
        query = body.query
        num_cves = body.num_cves
        similar_cves = search_similar_cves_with_technique_descp(query, num_cves)
        return similar_cves
    except Exception as e:
        my_logger.error(f"Exception: {e}\n{traceback.format_exc()}")
        return []