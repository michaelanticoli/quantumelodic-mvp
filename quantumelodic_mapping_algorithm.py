#!/usr/bin/env python3
"""
Quantumelodic MetaSystem - Core Mapping Algorithm

This script demonstrates the core mapping algorithm that translates astrological data
into musical compositions, focusing on the fundamental transformation principles withoutf
requiring external astrological calculation libraries.

Key features:
- Planet to musical mode mapping
- Zodiac sign influence processing
- Aspect to musical interval mapping
- House influence application
- Basic composition structure generation

For a complete implementation, this would be integrated with Swiss Ephemeris for
accurate astrological calculations and Music21 for comprehensive music generation.
"""

import math
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# ======= Astrological Constants =======

# Zodiac signs and their starting degrees (0-based, 0-360 scale)
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Element associations for zodiac signs
SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

# Modality associations for zodiac signs
SIGN_MODALITIES = {
    "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
    "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
    "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable"
}

# Planet data - ID, name, and speed (degrees per day)
PLANETS = [
    {"id": 0, "name": "Sun", "speed": 1.0},
    {"id": 1, "name": "Moon", "speed": 13.2},
    {"id": 2, "name": "Mercury", "speed": 1.4},
    {"id": 3, "name": "Venus", "speed": 1.2},
    {"id": 4, "name": "Mars", "speed": 0.5},
    {"id": 5, "name": "Jupiter", "speed": 0.08},
    {"id": 6, "name": "Saturn", "speed": 0.03},
    {"id": 7, "name": "Uranus", "speed": 0.01},
    {"id": 8, "name": "Neptune", "speed": 0.006},
    {"id": 9, "name": "Pluto", "speed": 0.004}
]

# Major aspects and their angles
ASPECTS = {
    "Conjunction": 0,
    "Sextile": 60,
    "Square": 90,
    "Trine": 120,
    "Opposition": 180
}

# Standard orbs for aspects
ASPECT_ORBS = {
    "Conjunction": 8,
    "Sextile": 4,
    "Square": 6,
    "Trine": 7,
    "Opposition": 8
}

# ======= Musical Constants =======

# Musical modes
MODES = {
    "Ionian": [0, 2, 4, 5, 7, 9, 11],     # Major scale
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],    # Natural minor scale
    "Locrian": [0, 1, 3, 5, 6, 8, 10]
}

# Note frequencies (A4 = 440Hz standard tuning)
NOTE_FREQUENCIES = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, 
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88
}

# ======= Mapping Tables =======

# Planet to Mode Mapping (based on Quantumelodic MetaSystem)
PLANET_MODE_MAPPING = {
    "Sun": {"mode": "Ionian", "base_note": "E", "instruments": ["Trumpet", "French Horn"]},
    "Moon": {"mode": "Aeolian", "base_note": "F", "instruments": ["Piano", "Cello"]},
    "Mercury": {"mode": "Mixolydian", "base_note": "D", "instruments": ["Flute", "Clarinet", "Synth"]},
    "Venus": {"mode": "Lydian", "base_note": "G", "instruments": ["Violin", "Harp"]},
    "Mars": {"mode": "Phrygian", "base_note": "C", "instruments": ["Percussion", "Electric Guitar"]},
    "Jupiter": {"mode": "Lydian", "base_note": "A", "instruments": ["Trumpet", "Trombone"]},
    "Saturn": {"mode": "Dorian", "base_note": "B", "instruments": ["Bassoon", "Organ"]},
    "Uranus": {"mode": "Aeolian", "base_note": "Ab", "instruments": ["Synthesizer", "Electric Piano"]},
    "Neptune": {"mode": "Ionian", "base_note": "Bb", "instruments": ["Harp", "Synthesizer"]},
    "Pluto": {"mode": "Phrygian", "base_note": "Db", "instruments": ["Low Brass", "Percussion"]}
}

# Zodiac Sign Musical Characteristic Mapping
SIGN_MUSICAL_MAPPING = {
    # Fire signs - energetic, dynamic
    "Aries": {"tempo_mod": 1.3, "rhythm": "Sharp, staccato", "dynamics": "ff", "articulation": "Marcato"},
    "Leo": {"tempo_mod": 1.2, "rhythm": "Bold, dramatic", "dynamics": "f", "articulation": "Tenuto"},
    "Sagittarius": {"tempo_mod": 1.25, "rhythm": "Galloping, adventurous", "dynamics": "mf", "articulation": "Staccato"},
    
    # Earth signs - stable, grounded
    "Taurus": {"tempo_mod": 0.8, "rhythm": "Steady, sustained", "dynamics": "mp", "articulation": "Legato"},
    "Virgo": {"tempo_mod": 0.9, "rhythm": "Precise, detailed", "dynamics": "p", "articulation": "Non-legato"},
    "Capricorn": {"tempo_mod": 0.75, "rhythm": "Structured, disciplined", "dynamics": "mf", "articulation": "Pesante"},
    
    # Air signs - flowing, changeable
    "Gemini": {"tempo_mod": 1.1, "rhythm": "Quick, varied", "dynamics": "mp", "articulation": "Leggiero"},
    "Libra": {"tempo_mod": 1.0, "rhythm": "Balanced, harmonious", "dynamics": "p", "articulation": "Dolce"},
    "Aquarius": {"tempo_mod": 1.15, "rhythm": "Unpredictable, syncopated", "dynamics": "mf", "articulation": "Staccatissimo"},
    
    # Water signs - flowing, emotional
    "Cancer": {"tempo_mod": 0.85, "rhythm": "Flowing, emotional", "dynamics": "p", "articulation": "Legato"},
    "Scorpio": {"tempo_mod": 0.9, "rhythm": "Intense, sustained", "dynamics": "ff", "articulation": "Marcato"},
    "Pisces": {"tempo_mod": 0.8, "rhythm": "Dreamy, fluid", "dynamics": "pp", "articulation": "Legatissimo"}
}

# Aspect to Musical Interval Mapping
ASPECT_INTERVAL_MAPPING = {
    "Conjunction": {"interval": 0, "harmony": "Unison/Octave", "consonance": 1.0, "description": "Complete unity"},
    "Sextile": {"interval": 4, "harmony": "Major Third", "consonance": 0.8, "description": "Harmonious opportunity"},
    "Square": {"interval": 6, "harmony": "Tritone", "consonance": 0.2, "description": "Tense, challenging"},
    "Trine": {"interval": 7, "harmony": "Perfect Fifth", "consonance": 0.9, "description": "Harmonic flow"},
    "Opposition": {"interval": 12, "harmony": "Octave", "consonance": 0.5, "description": "Tense balance"}
}

# House to Musical Form Mapping
HOUSE_FORM_MAPPING = {
    1: {"section": "Introduction", "focus": "Theme", "emotion": "Self-expression", "dynamics": "f"},
    2: {"section": "Development", "focus": "Resources", "emotion": "Stability", "dynamics": "mp"},
    3: {"section": "Bridge", "focus": "Communication", "emotion": "Curiosity", "dynamics": "mf"},
    4: {"section": "Emotional Core", "focus": "Foundation", "emotion": "Security", "dynamics": "p"},
    5: {"section": "Exposition", "focus": "Creativity", "emotion": "Joy", "dynamics": "ff"},
    6: {"section": "Interlude", "focus": "Service", "emotion": "Analytical", "dynamics": "mp"},
    7: {"section": "Counterpoint", "focus": "Relationship", "emotion": "Balance", "dynamics": "mf"},
    8: {"section": "Transformation", "focus": "Depth", "emotion": "Intensity", "dynamics": "ff"},
    9: {"section": "Expansion", "focus": "Wisdom", "emotion": "Inspiration", "dynamics": "f"},
    10: {"section": "Climax", "focus": "Achievement", "emotion": "Authority", "dynamics": "ff"},
    11: {"section": "Variation", "focus": "Community", "emotion": "Innovation", "dynamics": "mf"},
    12: {"section": "Resolution", "focus": "Transcendence", "emotion": "Spiritual", "dynamics": "pp"}
}


# ======= Core Mapping Classes =======

class AstrologicalData:
    """Class to store and process astrological data"""
    
    def __init__(self, birth_data: Dict[str, Any] = None):
        """Initialize with birth data or empty state"""
        self.planets = []
        self.aspects = []
        self.houses = {}
        self.birth_data = birth_data or {}
        
    def set_planet_position(self, planet_id: int, position: float, retrograde: bool = False) -> None:
        """Set a planet's position in the zodiac (0-360 degrees)"""
        # Get planet info
        planet_info = next((p for p in PLANETS if p["id"] == planet_id), None)
        if not planet_info:
            raise ValueError(f"Invalid planet ID: {planet_id}")
        
        # Calculate zodiac sign
        sign_index = math.floor(position / 30)
        sign_position = position % 30
        zodiac_sign = ZODIAC_SIGNS[sign_index % 12]
        
        # Placeholder for house calculation (would use proper house system in full implementation)
        # Here we're just using a simple approximation
        house = (sign_index % 12) + 1
        
        # Add planet data
        self.planets.append({
            "id": planet_id,
            "name": planet_info["name"],
            "position": position,
            "sign": zodiac_sign,
            "sign_position": sign_position,
            "house": house,
            "retrograde": retrograde
        })
    
    def calculate_aspects(self) -> None:
        """Calculate aspects between planets"""
        self.aspects = []
        
        # Check each planet pair
        for i, planet1 in enumerate(self.planets):
            for j, planet2 in enumerate(self.planets):
                # Skip same planet and already processed pairs
                if i >= j:
                    continue
                
                # Calculate angular distance
                angle_diff = abs(planet1["position"] - planet2["position"]) % 360
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Check if this forms a valid aspect
                for aspect_name, aspect_angle in ASPECTS.items():
                    orb = abs(angle_diff - aspect_angle)
                    max_orb = ASPECT_ORBS[aspect_name]
                    
                    if orb <= max_orb:
                        # Calculate if aspect is applying or separating
                        # (Simplified - would consider retrograde motion in full implementation)
                        p1_speed = next((p["speed"] for p in PLANETS if p["name"] == planet1["name"]), 1)
                        p2_speed = next((p["speed"] for p in PLANETS if p["name"] == planet2["name"]), 1)
                        
                        # Basic applying/separating calculation
                        is_applying = False
                        if p1_speed > p2_speed:
                            is_applying = (planet1["position"] < planet2["position"]) == (aspect_angle < 180)
                        else:
                            is_applying = (planet1["position"] > planet2["position"]) == (aspect_angle < 180)
                        
                        # Add aspect
                        self.aspects.append({
                            "planet1": planet1["name"],
                            "planet2": planet2["name"],
                            "aspect": aspect_name,
                            "angle": aspect_angle,
                            "orb": orb,
                            "applying": is_applying,
                            # Strength is higher when orb is smaller
                            "strength": 1 - (orb / max_orb)
                        })
                        
                        # Only store the strongest aspect between two planets
                        break
    
    def generate_mock_chart(self) -> None:
        """Generate a mock astrological chart for demonstration purposes"""
        # Use current time to seed the mock chart
        now = datetime.now()
        seed = now.hour * 60 + now.minute
        
        # Set planet positions with some pseudo-random distribution
        for planet in PLANETS:
            # Generate a position based on planet ID and seed
            position = (planet["id"] * 30 + seed) % 360
            retrograde = (planet["id"] + seed) % 5 == 0  # 20% chance of retrograde
            
            self.set_planet_position(planet["id"], position, retrograde)
        
        # Calculate aspects between planets
        self.calculate_aspects()
    
    def get_planet_by_name(self, name: str) -> Optional[Dict]:
        """Get planet data by name"""
        return next((p for p in self.planets if p["name"] == name), None)


class MusicalMappingEngine:
    """Core engine that translates astrological data into musical parameters"""
    
    def __init__(self, chart_data: AstrologicalData):
        """Initialize with astrological chart data"""
        self.chart_data = chart_data
        self.musical_data = {
            "planets": [],
            "aspects": [],
            "composition": {
                "key": "C",
                "tempo": 100,
                "form": []
            }
        }
        self.base_tempo = 100  # BPM
    
    def map_planets_to_music(self) -> None:
        """Map planetary positions to musical parameters"""
        for planet_data in self.chart_data.planets:
            planet_name = planet_data["name"]
            sign = planet_data["sign"]
            house = planet_data["house"]
            
            # Get base musical mapping for this planet
            planet_mapping = PLANET_MODE_MAPPING.get(planet_name, {
                "mode": "Ionian",
                "base_note": "C",
                "instruments": ["Piano"]
            })
            
            # Get zodiac sign influences
            sign_mapping = SIGN_MUSICAL_MAPPING.get(sign, {
                "tempo_mod": 1.0,
                "rhythm": "Regular",
                "dynamics": "mf",
                "articulation": "Normal"
            })
            
            # Calculate adjusted tempo based on planet speed and zodiac sign
            planet_info = next((p for p in PLANETS if p["name"] == planet_name), {"speed": 1.0})
            speed_factor = min(2.0, max(0.5, math.log(planet_info["speed"] + 0.1) + 1.5))
            tempo = self.base_tempo * speed_factor * sign_mapping["tempo_mod"]
            
            # Apply retrograde modification if applicable
            if planet_data["retrograde"]:
                tempo *= 0.8  # Slower tempo for retrograde planets
                
            # Get house influence
            house_mapping = HOUSE_FORM_MAPPING.get(house, {
                "section": "Other",
                "focus": "General",
                "emotion": "Neutral",
                "dynamics": "mp"
            })
            
            # Build musical representation of this planet
            musical_planet = {
                "name": planet_name,
                "position": planet_data["position"],
                "sign": sign,
                "house": house,
                "retrograde": planet_data["retrograde"],
                "mode": planet_mapping["mode"],
                "base_note": planet_mapping["base_note"],
                "instruments": planet_mapping["instruments"],
                "tempo": tempo,
                "rhythm": sign_mapping["rhythm"],
                "dynamics": sign_mapping["dynamics"],
                "articulation": sign_mapping["articulation"],
                "section": house_mapping["section"],
                "emotion": house_mapping["emotion"]
            }
            
            self.musical_data["planets"].append(musical_planet)
    
    def map_aspects_to_intervals(self) -> None:
        """Map astrological aspects to musical intervals"""
        for aspect_data in self.chart_data.aspects:
            # Get musical mapping for this aspect
            aspect_name = aspect_data["aspect"]
            aspect_mapping = ASPECT_INTERVAL_MAPPING.get(aspect_name, {
                "interval": 0,
                "harmony": "Unison",
                "consonance": 0.5,
                "description": "Neutral"
            })
            
            # Get planet data
            planet1 = self.chart_data.get_planet_by_name(aspect_data["planet1"])
            planet2 = self.chart_data.get_planet_by_name(aspect_data["planet2"])
            
            if not planet1 or not planet2:
                continue
                
            # Calculate combined intensity based on planet and aspect
            intensity = aspect_data["strength"] * (0.7 + (planet1["house"] % 3) * 0.1)
            
            # Build musical representation of this aspect
            musical_aspect = {
                "planet1": aspect_data["planet1"],
                "planet2": aspect_data["planet2"],
                "aspect": aspect_name,
                "interval": aspect_mapping["interval"],
                "harmony": aspect_mapping["harmony"],
                "consonance": aspect_mapping["consonance"],
                "intensity": intensity,
                "applying": aspect_data["applying"],
                "description": aspect_mapping["description"]
            }
            
            self.musical_data["aspects"].append(musical_aspect)
    
    def determine_composition_structure(self) -> None:
        """Determine overall composition structure based on chart patterns"""
        # Find the most prominent houses
        house_count = {}
        for planet in self.chart_data.planets:
            house = planet["house"]
            house_count[house] = house_count.get(house, 0) + 1
        
        # Sort houses by planet count
        prominent_houses = sorted(house_count.items(), key=lambda x: x[1], reverse=True)
        
        # Create composition form based on prominent houses
        form = []
        for house, count in prominent_houses[:5]:  # Use top 5 houses for structure
            house_mapping = HOUSE_FORM_MAPPING.get(house, {
                "section": f"Section {house}",
                "focus": "General",
                "emotion": "Neutral",
                "dynamics": "mp"
            })
            
            # Planets in this house
            planets_in_house = [p for p in self.chart_data.planets if p["house"] == house]
            planet_names = [p["name"] for p in planets_in_house]
            
            form.append({
                "section": house_mapping["section"],
                "house": house,
                "planets": planet_names,
                "focus": house_mapping["focus"],
                "emotion": house_mapping["emotion"],
                "dynamics": house_mapping["dynamics"],
                "duration": 20 + count * 10  # Longer sections for houses with more planets
            })
        
        self.musical_data["composition"]["form"] = form
        
        # Determine overall key and tempo
        sun_data = self.chart_data.get_planet_by_name("Sun")
        moon_data = self.chart_data.get_planet_by_name("Moon")
        
        if sun_data:
            # Use Sun's position for the overall key
            sun_sign = sun_data["sign"]
            sun_mapping = PLANET_MODE_MAPPING["Sun"]
            self.musical_data["composition"]["key"] = sun_mapping["base_note"]
            self.musical_data["composition"]["mode"] = sun_mapping["mode"]
            
            # Adjust mode based on Sun's sign element
            element = SIGN_ELEMENTS.get(sun_sign)
            if element == "Fire":
                self.musical_data["composition"]["mode"] = "Lydian"  # Bright, energetic
            elif element == "Earth":
                self.musical_data["composition"]["mode"] = "Dorian"  # Stable, grounded
            elif element == "Air":
                self.musical_data["composition"]["mode"] = "Mixolydian"  # Mobile, intellectual
            elif element == "Water":
                self.musical_data["composition"]["mode"] = "Aeolian"  # Flowing, emotional
        
        if moon_data:
            # Use Moon's position to influence tempo
            moon_sign = moon_data["sign"]
            moon_sign_mapping = SIGN_MUSICAL_MAPPING.get(moon_sign, {"tempo_mod": 1.0})
            
            # Base tempo on Moon's sign influence
            self.musical_data["composition"]["tempo"] = self.base_tempo * moon_sign_mapping["tempo_mod"]
    
    def generate_note_sequence(self) -> List[Dict]:
        """Generate a sequence of notes based on the musical mappings"""
        notes = []
        
        # Generate a sequence for each planet
        for planet_data in self.musical_data["planets"]:
            # Get base note and mode
            base_note = planet_data["base_note"]
            mode_name = planet_data["mode"]
            mode_intervals = MODES.get(mode_name, MODES["Ionian"])
            
            # Generate a short motif for this planet
            motif_length = 4 + (planet_data["house"] % 4)  # 4-7 notes based on house
            
            for i in range(motif_length):
                # Choose interval from the mode
                interval_index = (i * 2) % len(mode_intervals)
                interval = mode_intervals[interval_index]
                
                # Calculate note properties
                duration = 0.5  # Quarter note
                if planet_data["rhythm"] == "Flowing, emotional" or planet_data["rhythm"] == "Dreamy, fluid":
                    duration = 1.0  # Half note
                elif planet_data["rhythm"] == "Sharp, staccato" or planet_data["rhythm"] == "Quick, varied":
                    duration = 0.25  # Eighth note
                
                # Apply retrograde modification if applicable
                if planet_data["retrograde"]:
                    # Reverse the sequence for retrograde planets
                    interval_index = len(mode_intervals) - 1 - interval_index
                    interval = mode_intervals[interval_index]
                
                # Add note
                notes.append({
                    "planet": planet_data["name"],
                    "note_index": interval,
                    "base_note": base_note,
                    "duration": duration,
                    "velocity": 0.7 if planet_data["dynamics"] == "mf" else 
                                0.9 if planet_data["dynamics"] in ["f", "ff"] else 0.5,
                    "articulation": planet_data["articulation"]
                })
        
        # Add notes representing aspects
        for aspect_data in self.musical_data["aspects"]:
            if aspect_data["consonance"] > 0.7:
                # Create harmonious interval for consonant aspects
                notes.append({
                    "planet": f"{aspect_data['planet1']}-{aspect_data['planet2']}",
                    "note_index": aspect_data["interval"],
                    "base_note": "C",  # Default base note
                    "duration": 1.0,  # Half note
                    "velocity": 0.6,
                    "articulation": "Legato"
                })
        
        return notes
    
    def process_chart(self) -> Dict:
        """Process the chart and generate complete musical mapping"""
        # Map planets to musical elements
        self.map_planets_to_music()
        
        # Map aspects to musical intervals
        self.map_aspects_to_intervals()
        
        # Determine overall composition structure
        self.determine_composition_structure()
        
        # Add a note sequence
        self.musical_data["notes"] = self.generate_note_sequence()
        
        return self.musical_data


# ======= Utility Functions =======

def note_number_to_name(note_index: int, base_note: str = "C") -> str:
    """Convert a note index (0-11) to a note name based on a base note"""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # Find base note index
    base_index = 0
    for i, note in enumerate(notes):
        if base_note.startswith(note):
            base_index = i
            break
    
    # Calculate resulting note
    result_index = (base_index + note_index) % 12
    return notes[result_index]


def note_to_frequency(note: str, octave: int = 4) -> float:
    """Convert a note name to its frequency"""
    if len(note) > 1 and note[1] in ["#", "b"]:
        note_name = note[:2]
    else:
        note_name = note[0]
    
    # Handle flats by converting to sharps
    if "b" in note_name:
        flat_map = {"Cb": "B", "Db": "C#", "Eb": "D#", "Fb": "E", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
        note_name = flat_map.get(note_name, note_name)
    
    # Get base frequency for this note
    base_freq = NOTE_FREQUENCIES.get(note_name, 440.0)  # Default to A
    
    # Adjust for octave (A4 = 440Hz)
    if note_name in ["A", "A#", "B"]:
        return base_freq * (2 ** (octave - 4))
    else:
        return base_freq * (2 ** (octave - 3))


def print_musical_data(musical_data: Dict) -> None:
    """Pretty print the musical data for demonstration"""
    print("\n===== QUANTUMELODIC METASYSTEM: CHART TO MUSIC MAPPING =====\n")
    
    # Print composition overview
    comp = musical_data["composition"]
    print(f"COMPOSITION OVERVIEW:")
    print(f"Key: {comp['key']} {comp.get('mode', 'Major')}")
    print(f"Tempo: {comp['tempo']:.1f} BPM")
    print("\nFORM STRUCTURE:")
    
    for i, section in enumerate(comp["form"]):
        print(f"  {i+1}. {section['section']} (House {section['house']}) - {section['emotion']}")
        print(f"     Planets: {', '.join(section['planets'])}")
        print(f"     Dynamics: {section['dynamics']}, Duration: {section['duration']}s")
    
    # Print planet mappings
    print("\nPLANETARY MUSICAL MAPPINGS:")
    for planet in musical_data["planets"]:
        print(f"\n  {planet['name']} in {planet['sign']} (House {planet['house']})")
        print(f"    {'RETROGRADE, ' if planet['retrograde'] else ''}Mode: {planet['mode']}, Base Note: {planet['base_note']}")
        print(f"    Instruments: {', '.join(planet['instruments'])}")
        print(f"    Tempo: {planet['tempo']:.1f} BPM, Rhythm: {planet['rhythm']}")
        print(f"    Dynamics: {planet['dynamics']}, Articulation: {planet['articulation']}")
    
    # Print aspect mappings
    print("\nASPECT MUSICAL MAPPINGS:")
    for aspect in musical_data["aspects"]:
        print(f"\n  {aspect['planet1']} {aspect['aspect']} {aspect['planet2']}")
        print(f"    Musical Interval: {aspect['harmony']} ({aspect['interval']} semitones)")
        print(f"    Consonance: {aspect['consonance']:.1f}, Intensity: {aspect['intensity']:.1f}")
        print(f"    Description: {aspect['description']}, {'Applying' if aspect['applying'] else 'Separating'}")
    
    # Print sample notes
    if "notes" in musical_data and musical_data["notes"]:
        print("\nSAMPLE MUSICAL NOTES GENERATED:")
        for i, note in enumerate(musical_data["notes"][:10]):  # Show first 10 notes
            note_name = note_number_to_name(note["note_index"], note["base_note"])
            freq = note_to_frequency(note_name)
            print(f"  {i+1}. {note['planet']}: {note_name} ({freq:.1f}Hz), Duration: {note['duration']}s, "
                  f"Velocity: {note['velocity']}, Articulation: {note['articulation']}")
        
        if len(musical_data["notes"]) > 10:
            print(f"  ... and {len(musical_data['notes']) - 10} more notes")
    
    print("\n==========================================================\n")


# ======= Main Demonstration =======

def main():
    """Main demonstration function"""
    print("Quantumelodic MetaSystem - Core Mapping Algorithm Demonstration")
    print("-------------------------------------------------------------")
    print("This script demonstrates the fundamental algorithm that translates")
    print("astrological chart data into musical compositions.")
    
    # Create a chart with mock data
    chart = AstrologicalData()
    chart.generate_mock_chart()
    
    # Create mapping engine
    mapping_engine = MusicalMappingEngine(chart)
    
    # Process chart and generate musical data
    musical_data = mapping_engine.process_chart()
    
    # Print the results
    print_musical_data(musical_data)
    
    # Save musical data to JSON file for further processing
    with open("quantumelodic_output.json", "w") as f:
        json.dump(musical_data, f, indent=2)
    
    print(f"Musical mapping data saved to quantumelodic_output.json")
    print("This data could be used to generate MIDI files or audio in a complete implementation.")


if __name__ == "__main__":
    main()
