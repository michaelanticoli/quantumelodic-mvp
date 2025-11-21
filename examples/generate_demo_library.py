"""Generate a demo MIDI library from canonical pentatonic modes.

This script iterates the canonical pentatonic modes (from `mappings/`),
generates a small HarmonicResult for each mode (by creating a Chart stub
using the mode's `sign`), runs the harmonic engine, and exports a MIDI
file for each mode into `examples/demos/`.

Run with:
    PYTHONPATH=src ./.venv/bin/python3 examples/generate_demo_library.py
"""
from pathlib import Path
from typing import Dict, Any
import os

from harmonic_engine import data_loader
from harmonic_engine import engine
from midi_engine import generate_midi_from_result


class _ChartStub:
    def __init__(self, sign: str):
        self.sun_sign = sign
        self.moon_sign = sign
        self.rising_sign = sign
        self.positions = {}
        self.aspects = []


def main():
    out_dir = Path('examples') / 'demos'
    out_dir.mkdir(parents=True, exist_ok=True)

    pent_map: Dict[str, Dict[str, Any]] = data_loader.load_pentatonic_modes()
    if not pent_map:
        print('No pentatonic modes found in mappings; aborting.')
        return 1

    created = 0
    for mode_id, row in pent_map.items():
        sign = row.get('sign') or row.get('mode') or 'C'
        chart = _ChartStub(sign)
        result = engine.run_harmonic_engine(chart)

        out_path = out_dir / f"{mode_id}.mid"
        generate_midi_from_result(result, str(out_path))
        print(f'Wrote: {out_path}')
        created += 1

    print(f'Generated {created} demo MIDI files in {out_dir.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
