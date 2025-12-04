"""Utilities for building natal chart summaries and exporting CSV rows.

This module computes basic planetary sign positions using `skyfield` so
the Streamlit app can automatically populate the structured CSV fields the
user requested. The calculations prioritize resilience: if the ephemeris
file cannot be fetched or another runtime issue occurs, the helper will
gracefully fall back to placeholder values instead of crashing the UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pytz
from skyfield.api import Star, load, wgs84

SIGN_ORDER: List[str] = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGN_ELEMENTS = {
    "Aries": "Fire",
    "Leo": "Fire",
    "Sagittarius": "Fire",
    "Taurus": "Earth",
    "Virgo": "Earth",
    "Capricorn": "Earth",
    "Gemini": "Air",
    "Libra": "Air",
    "Aquarius": "Air",
    "Cancer": "Water",
    "Scorpio": "Water",
    "Pisces": "Water",
}

SIGN_MODALITIES = {
    "Aries": "Cardinal",
    "Cancer": "Cardinal",
    "Libra": "Cardinal",
    "Capricorn": "Cardinal",
    "Taurus": "Fixed",
    "Leo": "Fixed",
    "Scorpio": "Fixed",
    "Aquarius": "Fixed",
    "Gemini": "Mutable",
    "Virgo": "Mutable",
    "Sagittarius": "Mutable",
    "Pisces": "Mutable",
}

SIGN_DATE_RANGES = {
    "Aries": "Mar 21 - Apr 19",
    "Taurus": "Apr 20 - May 20",
    "Gemini": "May 21 - Jun 20",
    "Cancer": "Jun 21 - Jul 22",
    "Leo": "Jul 23 - Aug 22",
    "Virgo": "Aug 23 - Sep 22",
    "Libra": "Sep 23 - Oct 22",
    "Scorpio": "Oct 23 - Nov 21",
    "Sagittarius": "Nov 22 - Dec 21",
    "Capricorn": "Dec 22 - Jan 19",
    "Aquarius": "Jan 20 - Feb 18",
    "Pisces": "Feb 19 - Mar 20",
}

CHART_RULERS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Pluto",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Uranus",
    "Pisces": "Neptune",
}


@dataclass
class NatalInputs:
    """Normalized inputs from the Streamlit form."""

    name: str
    birth_datetime: datetime
    latitude: float
    longitude: float
    timezone: str = "UTC"


def _longitude_to_sign(longitude: float) -> Tuple[str, float]:
    """Convert an ecliptic longitude to a zodiac sign and degree within the sign."""

    normalized = longitude % 360
    sign_index = int(normalized // 30)
    degree_in_sign = normalized % 30
    return SIGN_ORDER[sign_index], degree_in_sign


def _best_match_ascendant(observer, ts_time) -> Tuple[str, float]:
    """Estimate the ascendant by scanning ecliptic points along the eastern horizon."""

    best_score = float("inf")
    best_longitude = 0.0
    for longitude in [x * 0.5 for x in range(0, 720)]:
        star = Star(ecliptic_latlon=(0.0, longitude))
        alt, az, _ = observer.at(ts_time).observe(star).apparent().altaz()
        score = abs(alt.degrees) + abs(az.degrees - 90)
        if score < best_score:
            best_score = score
            best_longitude = longitude

    return _longitude_to_sign(best_longitude)


def _dominant_element(planets: Dict[str, Dict[str, float]]) -> str:
    totals: Dict[str, float] = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
    weights = {"Sun": 3, "Moon": 3, "Ascendant": 3, "Mercury": 2, "Venus": 2, "Mars": 2}

    for planet, data in planets.items():
        element = SIGN_ELEMENTS.get(data.get("sign", ""), "Earth")
        totals[element] += weights.get(planet, 1)

    return max(totals, key=totals.get)


def _dominant_modality(planets: Dict[str, Dict[str, float]]) -> str:
    totals: Dict[str, float] = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}
    for data in planets.values():
        modality = SIGN_MODALITIES.get(data.get("sign", ""))
        if modality:
            totals[modality] += 1
    return max(totals, key=totals.get)


def _safe_load_ephemeris() -> Optional[object]:
    """Attempt to load the JPL DE421 ephemeris.

    Returns `None` when the ephemeris cannot be fetched so callers can
    gracefully fall back to placeholder data instead of raising.
    """

    try:
        return load("de421.bsp")
    except Exception:  # pragma: no cover - defensive guard
        return None


def _placeholder_planets() -> Dict[str, Dict[str, float]]:
    """Return a placeholder planet map when computation is unavailable."""

    placeholder = {
        name: {"sign": "Unknown", "degree": 0.0}
        for name in [
            "Sun",
            "Moon",
            "Mercury",
            "Venus",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
            "Pluto",
        ]
    }
    placeholder["Ascendant"] = {"sign": "Unknown", "degree": 0.0}
    return placeholder


def compute_natal_chart(inputs: NatalInputs) -> Dict[str, Dict[str, float]]:
    """Compute planet positions and ascendant for the provided inputs."""

    ephemeris = _safe_load_ephemeris()
    if ephemeris is None:
        return _placeholder_planets()

    try:
        ts = load.timescale()
        timezone = pytz.timezone(inputs.timezone)
        localized_dt = timezone.localize(inputs.birth_datetime)
        ts_time = ts.from_datetime(localized_dt.astimezone(pytz.UTC))
        observer = wgs84.latlon(inputs.latitude, inputs.longitude)

        bodies = {
            "Sun": ephemeris["sun"],
            "Moon": ephemeris["moon"],
            "Mercury": ephemeris["mercury"],
            "Venus": ephemeris["venus"],
            "Mars": ephemeris["mars"],
            "Jupiter": ephemeris["jupiter barycenter"],
            "Saturn": ephemeris["saturn barycenter"],
            "Uranus": ephemeris["uranus barycenter"],
            "Neptune": ephemeris["neptune barycenter"],
            "Pluto": ephemeris["pluto barycenter"],
        }

        planets: Dict[str, Dict[str, float]] = {}
        for name, target in bodies.items():
            astrometric = observer.at(ts_time).observe(target)
            ecliptic_lon = astrometric.apparent().ecliptic_latlon()[1].degrees
            sign, degree = _longitude_to_sign(ecliptic_lon)
            planets[name] = {"sign": sign, "degree": degree}

        asc_sign, asc_degree = _best_match_ascendant(observer, ts_time)
        planets["Ascendant"] = {"sign": asc_sign, "degree": asc_degree}

        return planets
    except Exception:  # pragma: no cover - defensive guard
        return _placeholder_planets()


def build_csv_row(planets: Dict[str, Dict[str, float]], inputs: NatalInputs) -> Dict[str, str]:
    """Construct the CSV row according to the requested schema."""

    sun_sign = planets.get("Sun", {}).get("sign", "Unknown")
    moon_sign = planets.get("Moon", {}).get("sign", "Unknown")
    rising_sign = planets.get("Ascendant", {}).get("sign", "Unknown")

    dominant_element = _dominant_element(planets)
    dominant_modality = _dominant_modality(planets)
    chart_ruler = CHART_RULERS.get(rising_sign, "")

    def planet_sign(planet: str) -> str:
        return planets.get(planet, {}).get("sign", "Unknown")

    return {
        "Name": inputs.name,
        "SunSign": sun_sign,
        "MoonSign": moon_sign,
        "Rising": rising_sign,
        "DateRange": SIGN_DATE_RANGES.get(sun_sign, ""),
        "Mercury": planet_sign("Mercury"),
        "Venus": planet_sign("Venus"),
        "Mars": planet_sign("Mars"),
        "Jupiter": planet_sign("Jupiter"),
        "Saturn": planet_sign("Saturn"),
        "Uranus": planet_sign("Uranus"),
        "Neptune": planet_sign("Neptune"),
        "Pluto": planet_sign("Pluto"),
        "NorthNode": "Calculated node data unavailable in offline mode",
        "Chiron": "Calculated Chiron data unavailable in offline mode",
        "Element": dominant_element,
        "Modality": dominant_modality,
        "DominantPlanet": "Sun" if sun_sign else "",
        "ChartRuler": chart_ruler,
        "SoulPurpose": f"Evolve through {sun_sign} virtues while rising as {rising_sign}.",
        "ShadowWork": f"Integrate the lessons of {planet_sign('Pluto')} and {planet_sign('Saturn')}.",
        "LifeLesson": f"Discipline of {planet_sign('Saturn')} in a {dominant_modality} path.",
        "CoreWound": "Chiron themes require further calculation.",
        "GiftToWorld": f"Jupiter in {planet_sign('Jupiter')} expands your influence.",
    }