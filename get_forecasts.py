import json

with open('forecast.json') as f:
    forecast = json.load(f)

for i, f in enumerate(forecast['forecasts']):
    del f['summary']
    for r in f['detailed']['reports']:
        del r['enhancedWeatherDescription']
        del r['precipitationProbabilityText']
        del r['weatherTypeText']
        del r['windDescription']
        del r['windDirectionFull']
    forecast['forecasts'][i] = forecast['forecasts'][i]['detailed']

with open('forecasts.json', 'w') as f:
    json.dump(forecast['forecasts'], f, indent=4, sort_keys=True)
