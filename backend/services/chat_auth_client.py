import os
from dotenv import load_dotenv
from openai import AzureOpenAI
load_dotenv()

api_key = os.getenv('AZURE_OPENAI_API_KEY')
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

if api_key is None or azure_endpoint is None:
    raise ValueError("API key or endpoint not found in environment variables!")


class Client:
    cnt = AzureOpenAI(
        api_key=api_key,  
        api_version="2024-10-21",
        azure_endpoint=azure_endpoint
    )
