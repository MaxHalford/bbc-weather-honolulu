
import json
import sqlite3
import git
import pandas as pd
from rich import progress


DATA_BRANCH = 'data'
FORECASTS_FILE = 'forecasts.json'
FORECASTS_TABLE = 'forecasts'
OBSERVATIONS_FILE = 'observations.json'
OBSERVATIONS_TABLE = 'observations'
SQLITE_PATH = 'bbc_weather.sqlite'


def load_forecasts_from_commit(commit: git.Commit) -> pd.DataFrame:

    try:
        blob = [b for b in commit.tree.blobs if b.name == FORECASTS_FILE][0]
    except IndexError:
        raise FileNotFoundError
    content = blob.data_stream.read().decode('utf8')
    forecasts = json.loads(content)
    reports = pd.DataFrame.from_dict(
        {**report, 'issueDate': frame['issueDate']}
        for frame in forecasts
        for report in frame['reports']
    )

    # Sanity checks
    assert reports['timeslotLength'].eq(1).all()
    assert reports.groupby(['issueDate', 'localDate', 'timeslot']).size().eq(1).all()

    # Sort out time stuff
    reports['issueDate'] = pd.to_datetime(reports['issueDate'])
    local_time_zone = reports['issueDate'].dt.tz
    at_date = pd.to_datetime(reports['localDate']).dt.tz_localize(local_time_zone)
    at_hour = pd.to_timedelta(reports['timeslot'].str.slice(0, 2).astype(int), unit='hours')
    reports['at'] = at_date + at_hour

    reports = reports[[
        'issueDate',
        'at',
        'temperatureC',
        'feelsLikeTemperatureC',
        'windSpeedKph'
    ]]

    reports = reports.rename(columns={
        'issueDate': 'issued_at',
        'temperatureC': 'celsius',
        'feelsLikeTemperatureC': 'feels_like_celsius',
        'windSpeedKph': 'wind_speed_kph'
    })

    return reports


def load_observations_from_commit(commit: git.Commit) -> pd.DataFrame:

    try:
        blob = [b for b in commit.tree.blobs if b.name == OBSERVATIONS_FILE][0]
    except IndexError:
        raise FileNotFoundError
    content = blob.data_stream.read().decode('utf8')
    observations = pd.json_normalize(json.loads(content))

    observations['at'] = (
        pd.to_datetime(observations['time.utc'])
        .dt.tz_convert(observations['time.timezone'].iloc[0])
    )

    # Sanity checks
    assert observations['at'].is_monotonic
    assert observations['at'].nunique() == len(observations)

    observations = observations[[
        'at',
        'temperature.c',
        'averageWindSpeed.kph'
    ]]

    observations = observations.rename(columns={
        'temperature.c': 'celsius',
        'averageWindSpeed.kph': 'wind_speed_kph'
    })

    return observations


if __name__ == '__main__':

    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    commits = list(git.Repo('.').iter_commits(DATA_BRANCH))

    # Forecasts
    if_exists = 'replace'
    for commit in progress.track(commits, description='Doing forecasts', transient=True):
        try:
            forecasts = load_forecasts_from_commit(commit)
        except FileNotFoundError:
            continue

        forecasts = forecasts.set_index(['issued_at', 'at'])
        forecasts.to_sql(name=FORECASTS_TABLE, con=sqlite_conn, if_exists=if_exists)
        if_exists = 'append'

    # Observations
    if_exists = 'replace'
    latest_at = None
    for commit in progress.track(commits, description='Doing observations', transient=True):
        try:
            observations = load_observations_from_commit(commit)
        except FileNotFoundError:
            continue

        if latest_at:
            observations = observations[observations['at'] > latest_at]

        if len(observations):
            latest_at = observations['at'].iloc[-1]
            observations = observations.set_index(['at'])
            observations.to_sql(name=OBSERVATIONS_TABLE, con=sqlite_conn, if_exists=if_exists)
            if_exists = 'append'
