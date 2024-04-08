import json
import http.client

def fetch_pokemon_list():
    conn = http.client.HTTPSConnection("pokeapi.co")
    conn.request("GET", "/api/v2/pokemon?limit=100&offset=0")
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        pokemon_list = json.loads(data)["results"]
        for pokemon in pokemon_list:
            pokemon_url = pokemon["url"]
            pokemon_id = int(pokemon_url.split("/")[-2])
            pokemon["id"] = pokemon_id
        return pokemon_list
    else:
        return {"error": "Failed to fetch data from PokeAPI."}

def fetch_pokemon_details(pokemon_id):
    conn = http.client.HTTPSConnection("pokeapi.co")
    conn.request("GET", f"/api/v2/pokemon/{pokemon_id}")
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        pokemon_data = json.loads(data)
        details = {
            "stat": pokemon_data["stats"],
            "weight": pokemon_data["weight"],
            "species": pokemon_data["species"],
            "abilities": pokemon_data["abilities"],
            "moves": pokemon_data["moves"][:2]  # Taking the first two moves
        }
        return details
    else:
        return {"error": "Failed to fetch data from PokeAPI."}

def lambda_handler(event, context):
    if event.get('path') == '/pokemon/summary' and event.get('httpMethod') == 'GET':
        pokemon_list = fetch_pokemon_list()
        return {
            'statusCode': 200,
            'body': json.dumps(pokemon_list)
        }
    elif event.get('path', '').startswith('/pokemon/details/') and event.get('httpMethod') == 'GET':
        pokemon_id = event['path'].split('/')[-1]
        pokemon_details = fetch_pokemon_details(pokemon_id)
        return {
            'statusCode': 200,
            'body': json.dumps(pokemon_details)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({"error": "Invalid endpoint."})
        }
