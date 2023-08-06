from enum import Enum


class TokenHeader(str, Enum):
    # To use for internal endpoint
    API_TOKEN = "X-Bedrock-Api-Token"
    # To access API through ui, using auth0 server or admin api, user vault issued token
    AUTH_SERVER_TOKEN = "Authorization"
    # To call the API directly (cURL, etc.)
    USER_ACCESS_TOKEN = "X-Bedrock-Access-Token"
