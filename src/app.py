from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.cache_layer import get, init_cache

app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/{path:path}")
async def proxy_to_pokeapi(path: str, request: Request):
    params = request.query_params
    return get(f"{path}{f"?{params}" if params else ""}")


@app.on_event("startup")
async def startup_hook():
    init_cache()
