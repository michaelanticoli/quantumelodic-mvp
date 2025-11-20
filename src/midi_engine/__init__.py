"""MIDI engine public API.

Provides `generate_midi_from_result(result, out_path)` which converts a
`HarmonicResult` (from `harmonic_engine.models`) into a short .mid file.
"""
from .scale_generator import generate_scale_notes
from .composition_builder import build_arpeggio_track, build_bass_track, Composition
from .exporter import export_composition
from harmonic_engine import data_loader


ELEMENT_ROOT = {
    'Fire': 62,   # D4
    'Earth': 60,  # C4
    'Air': 64,    # E4
    'Water': 65,  # F4
}


def generate_midi_from_result(result, out_path: str):
    """Create a simple MIDI file from a HarmonicResult.

    - Looks up semitone patterns for the reported primary pentatonic / quadratonic
      mode IDs in the canonical mappings.
    - Generates two tracks: arpeggio and bass, and exports to `out_path`.
    """
    pent_map = data_loader.load_pentatonic_modes()
    quad_map = data_loader.load_quadratonic_modes()

    pent_mode = pent_map.get(result.primary_pentatonic_mode)
    quad_mode = quad_map.get(result.primary_quadratonic_mode)

    # prefer pentatonic pattern if available, else quadratonic
    semitone_pattern = None
    if pent_mode:
        semitone_pattern = pent_mode.get('semitone_pattern')
    if not semitone_pattern and quad_mode:
        semitone_pattern = quad_mode.get('semitone_pattern')
    if not semitone_pattern:
        semitone_pattern = '2-2-3-2-3'

    root = ELEMENT_ROOT.get(result.dominant_element, 60)

    notes = generate_scale_notes(root, semitone_pattern, octaves=2)

    arpeggio = build_arpeggio_track('lead', notes, repeats=8, note_length=0.5)
    bass = build_bass_track('bass', notes, repeats=8, note_length=2.0)

    comp = Composition(tracks=[arpeggio, bass], tempo_bpm=result.sonic_payload.recommended_tempo_bpm)

    export_composition(comp, out_path)

    return out_path
