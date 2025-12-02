from math import fmod
from itertools import combinations

SIGN_NAMES = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]
SIGN_ELEMENTS = {
    "Aries":"Fire","Taurus":"Earth","Gemini":"Air","Cancer":"Water",
    "Leo":"Fire","Virgo":"Earth","Libra":"Air","Scorpio":"Water",
    "Sagittarius":"Fire","Capricorn":"Earth","Aquarius":"Air","Pisces":"Water"
}

MAJOR_ASPECTS = [
    (0, "Conjunction"),
    (60, "Sextile"),
    (90, "Square"),
    (120, "Trine"),
    (150, "Quincunx"),
    (180, "Opposition"),
]

def normalize(angle):
    return angle % 360

def angle_diff(a, b):
    d = abs(normalize(a) - normalize(b))
    if d > 180:
        d = 360 - d
    return d

def long_to_sign_degree(lon):
    lon = normalize(lon)
    sign_index = int(lon // 30)
    deg_in_sign = lon - (sign_index * 30)
    return SIGN_NAMES[sign_index], round(deg_in_sign, 2), sign_index

def _try_get_planet_positions(chart):
    possibilities = []
    if hasattr(chart, "planets"):
        p = getattr(chart, "planets")
        if isinstance(p, dict):
            for name, val in p.items():
                if isinstance(val, (int, float)):
                    possibilities.append({"name": name, "lon": float(val)})
                else:
                    lon = getattr(val, "longitude", None) or getattr(val, "lon", None) or (val.get("longitude") if isinstance(val, dict) else None)
                    house = getattr(val, "house", None) or getattr(val, "house_no", None) or (val.get("house") if isinstance(val, dict) else None)
                    d = {"name": name}
                    if lon is not None:
                        d["lon"] = float(lon)
                    if house is not None:
                        try:
                            d["house"] = int(house)
                        except Exception:
                            pass
                    possibilities.append(d)
            return possibilities
        if isinstance(p, list):
            for item in p:
                name = getattr(item, "name", None) or (item.get("name") if isinstance(item, dict) else None)
                lon = getattr(item, "longitude", None) or getattr(item, "lon", None) or (item.get("longitude") if isinstance(item, dict) else None)
                house = getattr(item, "house", None) or (item.get("house") if isinstance(item, dict) else None)
                if name and lon is not None:
                    d = {"name": name, "lon": float(lon)}
                    if house is not None:
                        try:
                            d["house"] = int(house)
                        except Exception:
                            pass
                    possibilities.append(d)
            if possibilities:
                return possibilities

    for attr in ("positions", "bodies", "objects", "planets_positions"):
        if hasattr(chart, attr):
            p = getattr(chart, attr)
            if isinstance(p, dict):
                for name, lon in p.items():
                    try:
                        possibilities.append({"name": name, "lon": float(lon)})
                    except Exception:
                        pass
            elif isinstance(p, list):
                for item in p:
                    if isinstance(item, tuple) and len(item) >= 2:
                        name, lon = item[0], item[1]
                        possibilities.append({"name": name, "lon": float(lon)})
                    else:
                        name = getattr(item, "name", None) or (item.get("name") if isinstance(item, dict) else None)
                        lon = getattr(item, "lon", None) or getattr(item, "longitude", None) or (item.get("longitude") if isinstance(item, dict) else None)
                        if name and lon is not None:
                            possibilities.append({"name": name, "lon": float(lon)})
            if possibilities:
                return possibilities

    common_planets = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto","TrueNode","Node","Chiron"]
    for p in common_planets:
        for fmt in (p, p.lower(), p.upper()):
            if hasattr(chart, fmt):
                val = getattr(chart, fmt)
                lon = getattr(val, "longitude", None) or getattr(val, "lon", None) or (val.get("longitude") if isinstance(val, dict) else None)
                if lon is not None:
                    possibilities.append({"name": p, "lon": float(lon)})
    return possibilities

def detect_aspects(planet_list, orb=8.0):
    out = []
    n = len(planet_list)
    for i in range(n):
        a = planet_list[i]
        for j in range(i+1, n):
            b = planet_list[j]
            diff = angle_diff(a["lon"], b["lon"])
            for angle, label in MAJOR_ASPECTS:
                if abs(diff - angle) <= orb:
                    out.append({
                        "p1": a["name"],
                        "p2": b["name"],
                        "aspect": label,
                        "angle": round(diff, 2),
                        "exactness": round(abs(diff - angle), 2)
                    })
                    break
    return out

def houses_for_planets(chart, planet_list):
    houses = []
    if any("house" in p for p in planet_list):
        return [{**p} for p in planet_list]

    if hasattr(chart, "houses"):
        ch = getattr(chart, "houses")
        cusp_map = {}
        if isinstance(ch, dict):
            cusp_map = {int(k): float(v) for k, v in ch.items()}
        elif isinstance(ch, list):
            for idx, val in enumerate(ch):
                try:
                    cusp_map[idx+1] = float(val)
                except Exception:
                    pass
        if cusp_map:
            for p in planet_list:
                lon = normalize(p["lon"])
                house = None
                for h in range(1,13):
                    start = cusp_map.get(h)
                    end = cusp_map.get(h%12 + 1)
                    if start is None or end is None:
                        continue
                    start = normalize(start)
                    end = normalize(end)
                    if start < end:
                        if lon >= start and lon < end:
                            house = h
                            break
                    else:
                        if lon >= start or lon < end:
                            house = h
                            break
                p2 = dict(p)
                p2["house"] = house
                houses.append(p2)
            return houses

    return [{**p} for p in planet_list]

def angular_strength(planet_list):
    counts = {"angular":0, "houses":{}}
    for p in planet_list:
        h = p.get("house")
        if h:
            counts["houses"].setdefault(h, 0)
            counts["houses"][h] += 1
            if h in (1,4,7,10):
                counts["angular"] += 1
    return counts

def house_counts(planet_list):
    counts = {i:0 for i in range(1,13)}
    for p in planet_list:
        h = p.get("house")
        if h:
            counts[h] = counts.get(h,0) + 1
    return counts

def stellium_houses(planet_list, threshold=3):
    groups = {}
    for p in planet_list:
        h = p.get("house")
        if h:
            groups.setdefault(h, []).append(p["name"])
    return {h:names for h,names in groups.items() if len(names) >= threshold}

def detect_grand_trines(aspects, planet_list, orb=8.0):
    trine_pairs = set()
    for a in aspects:
        if a["aspect"] == "Trine":
            pair = tuple(sorted([a["p1"], a["p2"]]))
            trine_pairs.add(pair)
    planets = [p["name"] for p in planet_list]
    grand_trines = []
    for combo in combinations(planets, 3):
        pairs = [tuple(sorted((combo[0],combo[1]))), tuple(sorted((combo[0],combo[2]))), tuple(sorted((combo[1],combo[2])))]
        if all(pair in trine_pairs for pair in pairs):
            grand_trines.append(combo)
    return grand_trines

def detect_t_squares(aspects):
    opp_pairs = {}
    square_map = {}
    for a in aspects:
        if a["aspect"] == "Opposition":
            pair = tuple(sorted([a["p1"], a["p2"]]))
            opp_pairs.setdefault(pair, []).append(a)
        if a["aspect"] == "Square":
            square_map.setdefault(a["p1"], set()).add(a["p2"])
            square_map.setdefault(a["p2"], set()).add(a["p1"])
    t_squares = []
    for (p1, p2), _ in opp_pairs.items():
        for apex, squares in square_map.items():
            if p1 in squares and p2 in squares:
                t_squares.append({"apex": apex, "opposition": (p1,p2)})
    return t_squares

def compute_insights(planet_list, aspect_list):
    element_counts = {"Fire":0,"Earth":0,"Air":0,"Water":0}
    sign_counts = {}
    for p in planet_list:
        sign, deg, idx = long_to_sign_degree(p["lon"])
        sign_counts.setdefault(sign, []).append(p["name"])
        element = SIGN_ELEMENTS.get(sign)
        if element:
            element_counts[element] += 1

    stellia = [ (s, names) for s, names in sign_counts.items() if len(names) >= 3 ]
    dominant_element = max(element_counts.items(), key=lambda kv: kv[1])[0] if element_counts else None
    dominant_sign = max(sign_counts.items(), key=lambda kv: len(kv[1]))[0] if sign_counts else None

    aspect_summary = {}
    for a in aspect_list:
        aspect_summary.setdefault(a["aspect"], 0)
        aspect_summary[a["aspect"]] += 1

    housecnts = house_counts(planet_list)
    stellia_by_house = stellium_houses(planet_list)
    angular = angular_strength(planet_list)
    grand_trines = detect_grand_trines(aspect_list, planet_list)
    t_squares = detect_t_squares(aspect_list)

    insights = {
        "element_counts": element_counts,
        "dominant_element": dominant_element,
        "dominant_sign": dominant_sign,
        "stellia_signs": stellia,
        "stellia_houses": stellia_by_house,
        "aspect_summary": aspect_summary,
        "house_counts": housecnts,
        "angular_strength": angular,
        "grand_trines": grand_trines,
        "t_squares": t_squares,
    }
    return insights

def detect_chart_type(chart):
    if hasattr(chart, "birth_date") or hasattr(chart, "birth_time") or getattr(chart, "source", None) == "natal":
        return "natal"
    if hasattr(chart, "time") and hasattr(chart, "date"):
        return "event"
    return "unknown"

def generate_report(chart, engine_result=None, orb=8.0):
    planets = _try_get_planet_positions(chart)
    planets = [ {"name": p["name"], "lon": float(p["lon"])} for p in planets if "lon" in p ]
    planets_with_houses = houses_for_planets(chart, planets)
    aspects = detect_aspects(planets_with_houses, orb=orb)
    insights = compute_insights(planets_with_houses, aspects)
    chart_type = detect_chart_type(chart)

    lines = []
    lines.append(f"Chart type: {chart_type}")
    lines.append("\nPlanets:")
    for p in planets_with_houses:
        sign, deg, si = long_to_sign_degree(p["lon"])
        house = p.get("house", "unknown")
        lines.append(f" - {p['name']}: {sign} {deg}° (lon {round(p['lon'],2)}°)  House: {house}")

    lines.append("\nAspects:")
    if not aspects:
        lines.append(" - (none detected within orb)")
    else:
        for a in aspects:
            lines.append(f" - {a['p1']} {a['aspect']} {a['p2']} (angle {a['angle']}°, dev {a['exactness']}°)")

    lines.append("\nInsights (summary):")
    lines.append(f" - Dominant element: {insights['dominant_element']}")
    lines.append(f" - Dominant sign: {insights['dominant_sign']}")
    if insights['stellia_signs']:
        for s,names in insights['stellia_signs']:
            lines.append(f" - Stellium in sign {s}: {', '.join(names)}")
    if insights['stellia_houses']:
        for h,names in insights['stellia_houses'].items():
            lines.append(f" - Stellium in house {h}: {', '.join(names)}")
    lines.append(f" - Element counts: {insights['element_counts']}")
    lines.append(f" - Aspect counts: {insights['aspect_summary']}")
    lines.append(f" - House counts: {insights['house_counts']}")
    lines.append(f" - Angular strength (planets in 1/4/7/10): {insights['angular_strength']['angular']}")

    if insights['grand_trines']:
        for gt in insights['grand_trines']:
            lines.append(f" - Grand Trine among: {', '.join(gt)}")
    if insights['t_squares']:
        for ts in insights['t_squares']:
            lines.append(f" - T-Square apex {ts['apex']} opposed to {ts['opposition'][0]} vs {ts['opposition'][1]}")

    if engine_result is not None:
        try:
            lines.append("\nEngine summary:")
            if hasattr(engine_result, "primary_pentatonic_mode"):
                lines.append(f" - Primary pentatonic mode: {engine_result.primary_pentatonic_mode}")
            if hasattr(engine_result, "primary_quadratonic_mode"):
                lines.append(f" - Primary quadratonic mode: {engine_result.primary_quadratonic_mode}")
            if hasattr(engine_result, "harmonic_tension_index"):
                lines.append(f" - Tension index: {engine_result.harmonic_tension_index}")
        except Exception:
            pass

    return {
        "json": {
            "chart_type": chart_type,
            "planets": planets_with_houses,
            "aspects": aspects,
            "insights": insights,
        },
        "text": "\n".join(lines)
    }
