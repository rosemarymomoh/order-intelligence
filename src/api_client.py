import os
from dotenv import load_dotenv
from commercetools.platform import Client
from commercetools import ClientCredentials

load_dotenv()

def get_commercetools_client():
    """Initialize commercetools client with credentials"""
    credentials = ClientCredentials(
        client_id=os.getenv('CTP_CLIENT_ID'),
        client_secret=os.getenv('CTP_CLIENT_SECRET')
    )
    
    client = Client(
        project_key=os.getenv('CTP_PROJECT_KEY'),
        credentials=credentials,
        auth_url=os.getenv('CTP_AUTH_URL'),
        api_url=os.getenv('CTP_API_URL')
    )
    return client

# Test the connection
if __name__ == "__main__":
    client = get_commercetools_client()
    project = client.project().get()
    print(f"Connected to project: {project.name}")