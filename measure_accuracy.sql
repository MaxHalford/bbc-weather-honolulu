WITH deltas AS (
    SELECT
        round((JulianDay(f.at) - JulianDay(f.issued_at)) * 24, 1) AS hours_ahead,
        o.celsius - f.celsius AS celsius,
        o.wind_speed_kph - f.wind_speed_kph AS wind_speed_kph
    FROM
        observations o,
        forecasts f
    WHERE o.at = f.at
)

SELECT
    hours_ahead,
    ROUND(AVG(ABS(celsius)), 2) AS mae_celsius,
    ROUND(AVG(ABS(wind_speed_kph)), 2) AS mae_kph_error
FROM deltas
GROUP BY hours_ahead;
