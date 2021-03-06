# Accuracy of BBC Weather forecasts for Honolulu

This repository records the forecasts made by [BBC Weather](https://www.bbc.com/weather) for the city of [Honolulu, USA](https://www.wikiwand.com/en/Honolulu). Essentially, there's a GitHub Action that runs at each half hour and saves the latest forecasts. The data is stored in a separate branch called `data`. Therefore, the data is versioned, which allows going back into the past to see the forecasts that were made in the past for any given hour in the (relative) future.

I made this after watching [Git scraping, the five minute lightning talk](https://simonwillison.net/2021/Mar/5/git-scraping/) by Simon Willison. It blew my mind!
