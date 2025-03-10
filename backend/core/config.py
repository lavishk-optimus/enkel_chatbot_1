import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
    AZURE_SEARCH_API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION")
    
    BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
    BLOB_CONTAINER_NAME = "blobl-test-1"
    
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    EMBEDDING_DEPLOYMENT_NAME = os.getenv("EMBEDDING_DEPLOYMENT_NAME")

    DATASOURCE_NAME = "srch-datasource-files"
    INDEX_NAME = "srch-index-files"
    SKILLSET_NAME = "srch-skillset-files"
    INDEXER_NAME = "srch-indexer-files"
