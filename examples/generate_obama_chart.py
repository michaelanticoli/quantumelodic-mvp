"""Generate Barack Obama's natal chart MIDI using the full pipeline.

Usage:
    PYTHONPATH=src ./.venv/bin/python3 examples/generate_obama_chart.py

This writes `examples/obama_natal_chart.mid`.
"""
import os
from pathlib import Path

from ephemeris_engine.chart_builder import build_chart_from_birth_data
from harmonic_engine import engine
from midi_engine import generate_midi_from_result


def main():
    out_dir = Path('examples')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'obama_natal_chart.mid'

    chart = build_chart_from_birth_data(
        date="1961-08-04",
        time="19:24",
        location_lat=21.3099,
        location_lon=-157.8581,
        timezone="Pacific/Honolulu",
    )

    result = engine.run_harmonic_engine(chart)

    generate_midi_from_result(result, str(out_path))

    print(f"Wrote MIDI: {out_path.resolve()}")


if __name__ == '__main__':
    main()
