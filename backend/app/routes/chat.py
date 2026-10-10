from fastapi import APIRouter, HTTPException, status
from app.models.chat import ChatQueryRequest, ChatQueryResponse
from app.services.orchestrator_service import route_user_query

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.post("", response_model=ChatQueryResponse)
async def chat(request: ChatQueryRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Query must not be empty."
        )
    try:
        response_text, agent_name = await route_user_query(query)
    except RuntimeError as exc:
        raise HTTPException( 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)) from exc
    return ChatQueryResponse(response=response_text, agent=agent_name)