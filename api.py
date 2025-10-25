from pydantic import BaseModel, ValidationError
import httpx
from typing import Dict, Any, List
from config import BASE_URL, API_KEY
import logging
import time

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    message: Message

class GrokResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Dict[str, Any]
    choices: List[Choice]

    class Config:
        extra = "allow"

class GrokAPIError(Exception):
    pass

class GrokAPI:

    def __init__(self):
        self.api_key = API_KEY
        self.client = httpx.Client(timeout=30.0, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.BASE_URL = BASE_URL

    def ask(
        self,
        messages: List[Dict],
        model: str = "grok-4-latest",
        stream: bool = False,
        temperature: float = 0.7
    ) -> GrokResponse:
        payload = {
        "messages": messages,
        "model": model,
        "stream" : stream,
        "temperature": temperature
        }

        retries = 0
        MAX_RETRIES = 3
        RETRY_DELAY = 2
        while retries < MAX_RETRIES:

            try:
                resp = self.client.post(self.BASE_URL, json=payload)
                resp.raise_for_status()
                data = resp.json()
                response = GrokResponse(**data)
                if not response.choices:
                    raise GrokAPIError("Empty response from API")
                return response

            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code >= 500:
                    retries += 1
                    time.sleep(RETRY_DELAY)
                    continue
                raise GrokAPIError(f"API error: {e.response.status_code} - {e.response.text}")
            
            except httpx.RequestError as e:
                logging.error(f"Network error: {e}")
                retries += 1
                time.sleep(RETRY_DELAY)
                continue
            except ValidationError as e:
                logging.error(f"Response validation error: {e}")
                raise GrokAPIError(f"Invalid response format: {e}")
            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                raise GrokAPIError(f"Unexpected error: {e}")
        raise GrokAPIError(f"Failed after {MAX_RETRIES} retries due to server errors.")
        
    def close(self):
        self.client.close()
