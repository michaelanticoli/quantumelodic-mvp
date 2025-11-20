from ephemeris_engine.chart_builder import build_chart_from_birth_data
from harmonic_engine.engine import run_harmonic_engine


def test_full_pipeline_integration():
    chart = build_chart_from_birth_data(
        date="1961-08-04",
        time="19:24",
        location_lat=21.3099,
        location_lon=-157.8581,
        timezone="Pacific/Honolulu"
    )

    result = run_harmonic_engine(chart)
    # Basic sanity checks
    assert chart.sun_sign == 'Leo'
    assert chart.moon_sign == 'Gemini'
    assert chart.rising_sign == 'Aquarius'
    assert isinstance(result.harmonic_tension_index, int)
