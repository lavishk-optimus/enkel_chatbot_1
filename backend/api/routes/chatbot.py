from fastapi import APIRouter
from backend.services.chatbot_service import query_index, generate_response
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from backend.core.config import Config
from azure.storage.blob import BlobServiceClient
from backend.services.azure_ai_search import create_datasource, create_index, create_indexer
from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str

router = APIRouter()    

@router.post("/chatbot/query")
def chatbot_query(request: ChatRequest):

    # # UNCOMMENT THE LINE BELOW after FIXING the query_index() from service.chatbot_service
    # rel_doc_text=query_index(question)
    rel_doc_text=request.question
    resp=generate_response(rel_doc_text)
    print(resp)

    return resp


 
# blob_service_client = BlobServiceClient.from_connection_string(Config.BLOB_CONNECTION_STRING)
# container_client = blob_service_client.get_container_client(Config.BLOB_CONTAINER_NAME)

# @router.post("/chatbot/upload")
# async def chatbot_upload_doc(file: UploadFile = File(...)):
#     try:
#         # Generate file path in Blob Storage
#         blob_name = file.filename
#         blob_client = container_client.get_blob_client(blob_name)
        
#         # Upload file to Azure Blob Storage
#         blob_client.upload_blob(file.file, overwrite=True)

#         return {"message": f"File '{file.filename}' uploaded successfully"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")





# Initialize Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(Config.BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(Config.BLOB_CONTAINER_NAME)

@router.post("/chatbot/upload")
async def chatbot_upload_doc(file: UploadFile = File(...)):
    try:
        # Upload file to Azure Blob Storage
        blob_name = file.filename
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.file, overwrite=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file to Blob Storage: {str(e)}")

    # Initialize response dictionary
    response = {"message": f"File '{file.filename}' uploaded successfully."}

    # Step 1: Create Datasource
    try:
        datasource_response = create_datasource()
        if "error" in datasource_response:
            raise Exception(datasource_response["error"])
        response["datasource_response"] = datasource_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create datasource: {str(e)}")

    # Step 2: Create Index
    try:
        index_response = create_index()
        if "error" in index_response:
            raise Exception(index_response["error"])
        response["index_response"] = index_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create index: {str(e)}")

    # Step 3: Create Indexer
    try:
        indexer_response = create_indexer()
        if "error" in indexer_response:
            raise Exception(indexer_response["error"])
        response["indexer_response"] = indexer_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create indexer_outer: {str(e)}")

    return response