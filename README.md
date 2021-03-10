# Accuracy of BBC Weather forecasts for Honolulu

This repository records the forecasts made by [BBC Weather](https://www.bbc.com/weather) for the city of [Honolulu, USA](https://www.wikiwand.com/en/Honolulu). Essentially, there's a GitHub Action that runs at each 30 minute mark and saves the latest forecasts. The data is stored in a separate branch called `data`. Therefore, the data is versioned. This allows going back into the past to see the forecasts that were made for any given hour in the (relative) future.

I made this after watching [Git scraping, the five minute lightning talk](https://simonwillison.net/2021/Mar/5/git-scraping/) by Simon Willison. It blew my mind! I agree with Simon that collecting and versioning API data via `git` is a powerful pattern. You could use this pattern to keep a ledger of any dynamic forecasting system, such as the predicted outcomes of football games. In these dynamical systems, the forecasts are updated when new information becomes available. Therefore, the forecasted values depend on the point in time when they were made. I think that it's super interesting to analyse how these forecasts evolve through time.

The `build_database.py` script iterates through all the commits in the `data` branch and consolidates the data into an SQLite database. You can run the script yourself by simply cloning this repository. Then, go into a terminal, navigate to the cloned repository, and install the necessary Python dependencies:

```sh
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Then, run the consolidation script:

```sh
python build_database.py
```

This will create a `bbc_weather.sqlite` file. You can load the latter into your preferred database access tool — I have a personal preference for [DataGrip](https://www.jetbrains.com/datagrip/) — to analyse the data. At present, the database contains two tables:

- `forecasts`: the predicted weather made at one point in time for a future point in time.
- `observations`: the actual weather values that occurred.

This project is MIT licensed.
