from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cache_layer import get

app = FastAPI()


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/{path:path}")
def proxy_to_pokeapi(path: str):
    return get(path)
