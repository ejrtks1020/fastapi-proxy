from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from common.database import engine
# from model.base_model import Base
# from model.user import user_model
# from common.config import api_router
import asyncio
from contextlib import asynccontextmanager
from icecream import ic
from util.request_util import RequestForwarder
import httpx
ic.configureOutput(includeContext=True)

# async def init_models():
#   async with engine.begin() as conn:
#     # await conn.run_sync(Base.metadata.drop_all)
#     await conn.run_sync(Base.metadata.create_all)

forwarder = RequestForwarder("http://localhost:5500")

@asynccontextmanager
async def lifespan(app: FastAPI):
    ic("start")
    # await init_models()

    yield

    ic("end")
    forwarder.close()

app = FastAPI(title="So Fast Project", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, Request

app = FastAPI()

@app.api_route(
    "/{full_path:path}", 
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]
)
async def catch_all(request: Request, full_path: str):
    ic(request.method, request.headers)
    body = await request.body()
    response = await forwarder.forward_request(
        method=request.method,
        path=full_path,
        headers=dict(request.headers),
        params=dict(request.query_params),
        body=body
    )

    ic("Status code:", response.status_code)
    if response.status_code == 204:
        ic("No content to process.")
    elif response.status_code != 200:
        ic("Request failed with status:", response.status_code)
    elif "application/json" in response.headers.get('Content-Type'):
        data = response.json()    
        # ic(data)
    else:
        ic(response.text)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )

# app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True, env_file='../env/.env.local')
