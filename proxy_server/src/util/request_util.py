import httpx
from fastapi import HTTPException

class RequestForwarder:
    def __init__(self, base_url: str):
      self.base_url = base_url
      self.client = httpx.AsyncClient()

    async def forward_request(
      self, 
      method: str, 
      path: str, 
      headers: dict, 
      params: dict, 
      body: bytes
    ):
      url = f"{self.base_url}/{path}"
      try:
        response = await self.client.request(
          method=method,
          url=url,
          headers=headers,
          params=params,
          content=body,
          timeout=10.0
        )
        return response
      except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting {url}. {str(e)}")

    async def close(self):
      await self.client.aclose()
