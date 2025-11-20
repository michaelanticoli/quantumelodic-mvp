from ephemeris_engine.chart_builder import build_chart_from_birth_data
from harmonic_engine.engine import run_harmonic_engine

# Build chart from birth data
chart = build_chart_from_birth_data(
    date="1961-08-04",
    time="19:24",
    location_lat=21.3099,
    location_lon=-157.8581,
    timezone="Pacific/Honolulu"
)

# Run through harmonic engine
result = run_harmonic_engine(chart)

print(f"\n=== Birth Chart ===")
print(f"Sun: {chart.sun_sign}")
print(f"Moon: {chart.moon_sign}")
print(f"Rising: {chart.rising_sign}")

print(f"\n=== Harmonic Analysis ===")
print(f"Primary Mode: {result.primary_pentatonic_mode}")
print(f"Behavioral Mode: {result.primary_quadratonic_mode}")
print(f"Tension Index: {result.harmonic_tension_index}/100")
print(f"Element: {result.dominant_element}")
print(f"Waveform: {result.sonic_payload.waveform}")
print(f"Tempo: {result.sonic_payload.recommended_tempo_bpm} BPM")
print(f"Timbres: {', '.join(result.sonic_payload.timbres[:3])}")
