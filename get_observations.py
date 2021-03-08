import json

with open('current.geojson') as f:
    geojson = json.load(f)
    try:
        obs = geojson['features'][0]['properties']['observations']
    except KeyError:
        obs = geojson['features'][1]['properties']['observations']

with open('observations.json', 'w') as f:
    json.dump(obs, f, indent=4, sort_keys=True)
