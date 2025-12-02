#!/usr/bin/env python3
import argparse
import json
from ephemeris_engine.chart_builder import build_chart_from_birth_data
from harmonic_engine.engine import run_harmonic_engine
from reporting.report import generate_report

def main():
    p = argparse.ArgumentParser(description="Run the harmonic pipeline for a birth record")
    p.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    p.add_argument("--time", required=True, help="Time (HH:MM)")
    p.add_argument("--lat", type=float, required=True, help="Latitude (decimal degrees)")
    p.add_argument("--lon", type=float, required=True, help="Longitude (decimal degrees)")
    p.add_argument("--tz", required=True, help="Timezone (IANA name, e.g. 'Pacific/Honolulu')")
    p.add_argument("--orb", type=float, default=8.0, help="Aspect orb in degrees")
    p.add_argument("--json", action="store_true", help="Print machine-readable JSON output")
    p.add_argument("--pretty", action="store_true", help="Print verbose human report plus detailed JSON")
    args = p.parse_args()

    chart = build_chart_from_birth_data(
        date=args.date,
        time=args.time,
        location_lat=args.lat,
        location_lon=args.lon,
        timezone=args.tz
    )

    result = run_harmonic_engine(chart)

    report = generate_report(chart, result, orb=args.orb)
    if args.json:
        print(json.dumps(report["json"], indent=2))
    elif args.pretty:
        print("="*70)
        print("HARMONIC REPORT (Human-friendly)")
        print("="*70)
        print(report["text"])
        print("\n" + "="*70)
        print("Detailed JSON")
        print("="*70)
        print(json.dumps(report["json"], indent=2))
    else:
        print(report["text"])

if __name__ == "__main__":
    main()
