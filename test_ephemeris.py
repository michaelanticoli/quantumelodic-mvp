from ephemeris_engine.chart_builder import build_chart_from_birth_data

# Barack Obama - known reference chart
chart = build_chart_from_birth_data(
    date="1961-08-04",
    time="19:24",
    location_lat=21.3099,
    location_lon=-157.8581,
    timezone="Pacific/Honolulu"
)

print(f"Sun: {chart.sun_sign}")      # Should be: Leo
print(f"Moon: {chart.moon_sign}")    # Should be: Gemini
print(f"Rising: {chart.rising_sign}") # Should be: Aquarius
print(f"Aspects found: {len(chart.aspects)}")
