from fastapi import APIRouter
import traceback
from .nl_to_sql_utils import get_similar_severities, get_most_relevant_severity, get_sql_query
from .nl_to_sql_prompts import tables_info
from pydantic import BaseModel

router = APIRouter()
    
class NLtoSQL(BaseModel):
    """Request body for streaming."""
    query: str

@router.post("/nl_to_sql")
async def nl_to_sql(body: NLtoSQL):
    try:
        query = body.query
        similar_severities = get_similar_severities(query)
        inputs = {
            "user_query":query,
            "severities":similar_severities
        }
        most_relevant_severity = await get_most_relevant_severity(inputs)
        inputs = {
            "tables_info":tables_info,
            "severity_value":most_relevant_severity
        }
        sql_query = await get_sql_query(inputs)
        return {
            "query": query,
            "most_relevant_severity": most_relevant_severity,
            "sql_query": sql_query
        }
    except Exception as e:
        traceback.print_exc()