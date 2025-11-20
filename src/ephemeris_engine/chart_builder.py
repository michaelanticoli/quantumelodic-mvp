"""
Chart builder that assembles a simple natal chart from birth data.

Provides `build_chart_from_birth_data()` which returns a small object
containing sun, moon, rising signs and found aspects.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import pytz

from .calculator import get_planet_positions, zodiac_sign_from_longitude, to_planetposition_dict
from .aspect_finder import find_aspects

try:
    import swisseph as swe
except Exception as e:
    raise ImportError("swisseph (pyswisseph) is required. Install with: pip install pyswisseph") from e


@dataclass
class Chart:
    sun_sign: str
    moon_sign: str
    rising_sign: str
    positions: Dict[str, Any]
    aspects: list


def build_chart_from_birth_data(date: str, time: str, location_lat: float, location_lon: float, timezone: str) -> Chart:
    """
    Build a simple natal chart.

    - `date` is YYYY-MM-DD
    - `time` is HH:MM (24h)
    - `location_lat` is latitude in degrees
    - `location_lon` is longitude (negative for west)
    - `timezone` is an IANA timezone string (e.g. 'Pacific/Honolulu')
    """
    # parse local datetime and convert to UTC
    local_tz = pytz.timezone(timezone)
    dt_local = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    dt_local = local_tz.localize(dt_local)
    dt_utc = dt_local.astimezone(pytz.utc)

    # Julian day in UT
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    jd_ut = swe.julday(year, month, day, hour)

    # Compute planet positions
    positions = get_planet_positions(jd_ut)

    # compute ascendant (rising) using houses: swe.houses(jd_ut, lat, lon)
    # Note: swe.houses expects geodetic longitude in degrees east (positive), so pass as-is
    try:
        cusps, ascmc = swe.houses(jd_ut, location_lat, location_lon)
        ascendant = ascmc[0]
    except Exception:
        # If houses fails, fallback to 0 deg
        ascendant = 0.0

    sun_sign = zodiac_sign_from_longitude(positions['Sun']['lon'])
    moon_sign = zodiac_sign_from_longitude(positions['Moon']['lon'])
    rising_sign = zodiac_sign_from_longitude(ascendant)

    aspects = find_aspects(positions)

    return Chart(
        sun_sign=sun_sign,
        moon_sign=moon_sign,
        rising_sign=rising_sign,
        positions=to_planetposition_dict(positions),
        aspects=aspects,
    )
