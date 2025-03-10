from fastapi import APIRouter
from backend.services.azure_ai_search import create_datasource, create_index, create_indexer

router = APIRouter()

@router.post("/indexing/datasource")
def trigger_create_datasource():
#    /cALL AZURE_AI_SERVICES RELEVENT DEFS CALL 
    return create_datasource()

@router.post("/indexing/index")
def trigger_create_index():
    return create_index()

@router.post("/indexing/indexer")
def trigger_create_indexer():
    return create_indexer()
