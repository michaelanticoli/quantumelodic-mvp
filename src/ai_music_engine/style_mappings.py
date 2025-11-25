"""Style mappings and helper conversions for AI prompt builder.

This module provides lookup dictionaries mapping modal ids/elements/planets
to descriptive style, timbre and instrument suggestions used when building
prompts for audio/text generation models.
"""
from typing import List

# Minimal canonical mappings for demo purposes. These can be extended
# from the Notion page referenced by the user.
MODAL_STYLES = {
    'PENT-ARIES-1': 'heroic electronic rock, driving rhythms, bright brass accents',
    'PENT-LEO-1': 'anthemic pop/indie with big synth leads and warm pads',
    'PENT-SAG-1': 'cinematic, open-ambient, expansive pads and bells',
    'PENT-TAURUS-1': 'downtempo soul, warm electric piano, lush strings',
    'PENT-VIRGO-1': 'minimal techno, precise arpeggios, mallet textures',
    'PENT-CAP-1': 'dark ambient, slow evolving drones and bass',
    'PENT-GEM-1': 'jazzy fusion, quick motifs, playful woodwinds',
    'PENT-LIB-1': 'smooth R&B, balanced harmonies, soft harp/pad textures',
    'PENT-AQU-1': 'glitch/IDM, synthetic textures and modular sequences',
    'PENT-CAN-1': 'lullaby-like ambient, soft piano and glassy pads',
    'PENT-SCOR-1': 'noir electronic, deep sub-bass and tension drones',
    'PENT-PIS-1': 'ambient choir, reverb-heavy soundscapes, gentle bells',
}

ELEMENT_DESCRIPTIONS = {
    'Fire': 'bright, aggressive timbres — brass stabs, distorted synth leads, high-energy percussion',
    'Earth': 'warm, grounded timbres — electric piano, mellow strings, plucked bass',
    'Air': 'light, airy timbres — flutes, chimes, shimmering pads',
    'Water': 'soft, rounded timbres — warm pads, glassy bells, reverb-heavy textures',
}

PLANET_INSTRUMENTS = {
    'Sun': ['lead synth', 'brass'],
    'Moon': ['pad', 'soft piano'],
    'Mercury': ['pluck synth', 'acoustic guitar'],
    'Venus': ['electric piano', 'warm pad'],
    'Mars': ['distorted guitar', 'taiko'],
    'Jupiter': ['orchestral brass', 'choir'],
    'Saturn': ['low organ', 'muted brass'],
    'Uranus': ['FM synth', 'glitch percussion'],
    'Neptune': ['choir pad', 'glass harmonics'],
    'Pluto': ['sub-bass', 'dark drone'],
}


def tension_to_dynamics(hti: int) -> str:
    """Map the harmonic tension index (0-100) to dynamics description."""
    if hti < 20:
        return 'very soft, sparse dynamics'
    if hti < 40:
        return 'soft, gentle dynamics'
    if hti < 60:
        return 'moderate dynamics, steady pulse'
    if hti < 80:
        return 'strong dynamics, pronounced accents'
    return 'very strong, aggressive dynamics with heavy impact'


def modal_to_genre_tags(mode_id: str, style_map: dict = None) -> List[str]:
    """Return a small list of genre/style tags for a modal id."""
    if style_map is None:
        style_map = MODAL_STYLES
    style = style_map.get(mode_id, '')
    if not style:
        return ['ambient']
    # pick a few keywords
    parts = [p.strip() for p in style.split(',')]
    tags = []
    for p in parts:
        # split on spaces and take first two words as tag candidates
        tokens = p.split()
        if not tokens:
            continue
        tag = tokens[0]
        if len(tokens) > 1:
            tag = f"{tokens[0]} {tokens[1]}"
        tags.append(tag.replace('/', '-'))
    return tags[:3]
