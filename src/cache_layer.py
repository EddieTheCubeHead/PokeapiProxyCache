import json

import requests
import sqlite3

API_URL = "https://pokeapi.co/api/v2"

cache: dict[str, dict | list[dict]] = {}
con = sqlite3.connect("cache_db.sqlite")


def replace_urls(raw_request_data: dict) -> dict:
    for key in raw_request_data:
        if type(raw_request_data[key]) is str:
            raw_request_data[key] = raw_request_data[key].replace("https://pokeapi.co/api/v2", "http://127.0.0.1:8000")
        elif (type(raw_request_data[key]) is list and len(raw_request_data[key]) > 0
              and type(raw_request_data[key][0]) is dict):
            for index, item in enumerate(raw_request_data[key]):
                raw_request_data[key][index] = replace_urls(item)
        elif type(raw_request_data[key]) is dict:
            raw_request_data[key] = replace_urls(raw_request_data[key])
    return raw_request_data


def try_get_from_database(request: str) -> dict | None:
    data = con.execute("SELECT Response FROM Requests WHERE Request = ?", (request,)).fetchone()
    return data if data is None else json.loads(data[0])


def add_to_database(request: str, response: dict):
    con.execute("INSERT INTO Requests (Request, Response) VALUES (?, ?)", (request, json.dumps(response)))
    con.commit()


def add_to_cache(request: str):
    data = try_get_from_database(request)
    if data is None:
        print("Fetching from PokeAPI")
        data = requests.get(f"{API_URL}/{request}").json()
        add_to_database(request, data)
    if type(data) is list:
        cache[request] = [replace_urls(item) for item in data]
    else:
        cache[request] = replace_urls(data)


def get(request: str) -> dict:
    if request not in cache:
        add_to_cache(request)
    return cache[request]


def init_cache():
    init_db()
    init_pokemon_cache()


def init_db():
    with open("src/create_table.sql", "r", encoding="utf-8") as script:
        con.execute(script.read())


def init_pokemon_cache():
    all_pokemon_json = requests.get("https://pokeapi.co/api/v2/pokemon?limit=9999").json()["results"]
    all_pokemon = [(pokemon["name"], int(pokemon["url"].split("/")[-2])) for pokemon in all_pokemon_json]
    for pokemon_name, pokemon_number in all_pokemon:
        print(f"Fetching data for {pokemon_name}, #{pokemon_number}")
        pokemon_data = get(f"pokemon/{pokemon_name}")
        get(f"pokemon-species/{pokemon_data['species']['url'].split('/')[-2]}")
