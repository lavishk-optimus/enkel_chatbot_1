import json
import requests
from backend.core.config import Config

headers = {"Content-Type": "application/json", "api-key": Config.AZURE_SEARCH_KEY}
params = {"api-version": Config.AZURE_SEARCH_API_VERSION}

# def create_datasource():
#     """Creates an Azure AI Search Data Source linked to Blob Storage."""
#     payload = {
#         "name": Config.DATASOURCE_NAME,
#         "type": "azureblob",
#         "credentials": {"connectionString": Config.BLOB_CONNECTION_STRING},
#         "container": {"name": Config.BLOB_CONTAINER_NAME},
#         "dataDeletionDetectionPolicy": {
#             "@odata.type": "#Microsoft.Azure.Search.NativeBlobSoftDeleteDeletionDetectionPolicy"
#         }
#     }
#     url = f"{Config.AZURE_SEARCH_ENDPOINT}/datasources/{Config.DATASOURCE_NAME}"
#     return requests.put(url, json=payload, headers=headers, params=params).json()

def create_datasource():
    """Creates an Azure AI Search Data Source linked to Blob Storage."""
    payload = {
        "name": Config.DATASOURCE_NAME,
        "type": "azureblob",
        "credentials": {"connectionString": Config.BLOB_CONNECTION_STRING},
        "container": {"name": Config.BLOB_CONTAINER_NAME},
        "dataDeletionDetectionPolicy": {
            "@odata.type": "#Microsoft.Azure.Search.NativeBlobSoftDeleteDeletionDetectionPolicy"
        }
    }
    url = f"{Config.AZURE_SEARCH_ENDPOINT}/datasources/{Config.DATASOURCE_NAME}"

    response = requests.put(url, json=payload, headers=headers, params=params)

    # Debugging print (Remove in production)
    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)

    if response.status_code == 204:
        return {"message": "Datasource already exists or was updated successfully."}

    if not response.text:
        raise Exception("Azure Search API returned an empty response.")

    try:
        return response.json()
    except json.JSONDecodeError:
        raise Exception(f"Failed to parse JSON response: {response.text}")


# def create_index():
#     """Creates an Azure AI Search Index."""
#     payload = {
#         "name": Config.INDEX_NAME,
#         "fields": [
#             {"name": "id", "type": "Edm.String", "key": True},
#             {"name": "title", "type": "Edm.String"},
#             {"name": "chunk", "type": "Edm.String"},
#             {"name": "chunkVector", "type": "Collection(Edm.Half)", "dimensions": 1536}
#         ],
#         "vectorSearch": {
#             "algorithms": [{"name": "use-hnsw", "kind": "hnsw"}],
#             "vectorizers": [{
#                 "name": "use-openai",
#                 "kind": "azureOpenAI",
#                 "azureOpenAIParameters": {
#                     "resourceUri": Config.AZURE_OPENAI_ENDPOINT,
#                     "apiKey": Config.AZURE_OPENAI_API_KEY,
#                     "deploymentId": Config.EMBEDDING_DEPLOYMENT_NAME
#                 }
#             }]
#         }
#     }
#     url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexes/{Config.INDEX_NAME}"
#     return requests.put(url, json=payload, headers=headers, params=params).json()

import requests
import json

def create_index():
    """Creates an Azure AI Search Index with proper vector search configuration for a free/basic tier."""
    payload = {
        "name": Config.INDEX_NAME,
        "vectorSearch": {
            "algorithms": [{"name": "use-hnsw", "kind": "hnsw"}],
            "compressions": [  # Optional compression
                {
                    "name": "use-scalar",
                    "kind": "scalarQuantization",
                    "rescoringOptions": {
                        "enableRescoring": "true",
                        "defaultOversampling": 10,
                        "rescoreStorageMethod": "preserveOriginals"
                    },
                    "scalarQuantizationParameters": {"quantizedDataType": "int8"},
                    "truncationDimension": 1024
                },
                {
                    "name": "use-binary",
                    "kind": "binaryQuantization",
                    "rescoringOptions": {
                        "enableRescoring": "true",
                        "defaultOversampling": 10,
                        "rescoreStorageMethod": "preserveOriginals"
                    },
                    "truncationDimension": 1024
                }
            ],
            "vectorizers": [{
                "name": "use-openai",
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": Config.AZURE_OPENAI_ENDPOINT,
                    "apiKey": Config.AZURE_OPENAI_API_KEY,
                    "deploymentId": Config.EMBEDDING_DEPLOYMENT_NAME,
                    "modelName": Config.EMBEDDING_DEPLOYMENT_NAME
                }
            }],
            "profiles": [  # Required for vector fields
                {
                    "name": "vector-profile-hnsw-scalar",
                    "compression": "use-scalar",
                    "algorithm": "use-hnsw",
                    "vectorizer": "use-openai"
                },
                {
                    "name": "vector-profile-hnsw-binary",
                    "compression": "use-binary",
                    "algorithm": "use-hnsw",
                    "vectorizer": "use-openai"
                }
            ]
        },
        "semantic": {  # Optional semantic search
            "configurations": [{
                "name": "my-semantic-config",
                "prioritizedFields": {
                    "titleField": {"fieldName": "title"},
                    "prioritizedContentFields": [{"fieldName": "chunk"}],
                    "prioritizedKeywordsFields": []
                }
            }]
        },
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "searchable": True, "retrievable": True},
            {"name": "title", "type": "Edm.String", "searchable": True, "retrievable": True},
            {"name": "chunk", "type": "Edm.String", "searchable": True, "retrievable": True},
            {
                "name": "chunkVector",
                "type": "Collection(Edm.Half)",
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-hnsw-scalar",  # Correct profile
                "searchable": True,
                "retrievable": False
            }
        ]
        # Uncomment for professionals
        # "cognitiveServices": {
        #     "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
        #     "description": Config.COG_SERVICES_NAME,
        #     "key": Config.COG_SERVICES_KEY
        # }
    }
    
    url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexes/{Config.INDEX_NAME}"
    

    try:
        response = requests.put(url, json=payload, headers=headers, params=params)
        print("Response Text:", response.text)  # Print detailed error message
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"detail": f"Failed to create index: {str(e)}"}

# def create_indexer():
#     """Creates an Indexer to process documents from Blob Storage."""
#     payload = {
#         "name": Config.INDEXER_NAME,
#         "dataSourceName": Config.DATASOURCE_NAME,
#         "targetIndexName": Config.INDEX_NAME,
#         "schedule": {"interval": "PT30M"},
#         "parameters": {
#             "configuration": {"dataToExtract": "contentAndMetadata"}
#         }
#     }
#     url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexers/{Config.INDEXER_NAME}"
#     return requests.put(url, json=payload, headers=headers, params=params).json()


import json
def create_indexer():
    """Creates an Indexer to process documents from Blob Storage."""
    payload = {
        "name": Config.INDEXER_NAME,
        "dataSourceName": Config.DATASOURCE_NAME,
        "targetIndexName": Config.INDEX_NAME,
        "schedule": {"interval": "PT30M"},
        "parameters": {
            "configuration": {"dataToExtract": "contentAndMetadata"}
        }
    }
    
    url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexers/{Config.INDEXER_NAME}?api-version=2023-07-01-Preview"

    print("Request URL:", url)
    print("Headers:", headers)
    print("Payload:", json.dumps(payload, indent=2))

    try:
        response = requests.put(url, json=payload, headers=headers)

        print("cr_indexer STATUS CODE:", response.status_code)

        if response.status_code == 204:  # No Content = Success
            return {"detail": "Indexer created successfully (204 No Content)"}

        response.raise_for_status()  # Raise error for 4xx/5xx responses

        return response.json() if response.content else {"detail": "Indexer created successfully, but no response body"}
    except requests.exceptions.RequestException as e:
        return {"detail": f"Failed to create indexer: {str(e)}"}
