import requests
from backend.core.config import Config
from backend.services.chat_auth_client import Client
client=Client().cnt


def query_index(question):
    """Queries the Azure AI Search Index."""
    payload = {
        "search": question,
        "top": 5,
        "searchFields": "title,chunk",
        "select": "id,title,chunk"
    }
    url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexes/{Config.INDEX_NAME}/docs/search"
    response = requests.post(url, json=payload, headers={"api-key": Config.AZURE_SEARCH_KEY})
    return response.json()



def generate_response(ques):
        resp=""
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": ques}
            ],
            stream=True
        )

        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end='',)
                resp=resp+chunk.choices[0].delta.content+" "
        
        # print(resp)
        return resp