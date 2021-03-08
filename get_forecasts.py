import json

with open('forecast.json') as f:
    forecast = json.load(f)

for f in forecast['forecasts']:
    del f['summary']
    for r in f['detailed']['reports']:
        del r['enhancedWeatherDescription']
        del r['precipitationProbabilityText']
        del r['weatherTypeText']
        del r['windDescription']
        del r['windDirectionFull']

with open('forecasts.json', 'w') as f:
    json.dump(forecast['forecasts'], f, indent=4, sort_keys=True)
