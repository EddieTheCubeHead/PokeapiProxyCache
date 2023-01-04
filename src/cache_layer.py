import requests


API_URL = "https://pokeapi.co/api/v2"


def get(path: str):
    return requests.get(f"{API_URL}/{path}").json()
