"""Simple composition builder: Note, Track and Composition helpers.

This module provides small helpers to build short patterns (arpeggios, basslines)
from a list of MIDI notes.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class Note:
    midi: int
    length_beats: float = 1.0
    velocity: int = 80


@dataclass
class Track:
    name: str
    notes: List[Note]


@dataclass
class Composition:
    tracks: List[Track]
    tempo_bpm: int = 90


def build_arpeggio_track(name: str, notes: List[int], repeats: int = 8, note_length: float = 0.5, velocity: int = 90) -> Track:
    seq: List[Note] = []
    for _ in range(repeats):
        for n in notes:
            seq.append(Note(midi=int(n), length_beats=note_length, velocity=velocity))
    return Track(name=name, notes=seq)


def build_bass_track(name: str, notes: List[int], repeats: int = 8, note_length: float = 2.0, velocity: int = 70) -> Track:
    # Use the first notes as bass root pattern (down an octave)
    seq: List[Note] = []
    bass_notes = [n - 12 for n in notes[:4]] if notes else [48]
    for _ in range(repeats):
        for n in bass_notes:
            seq.append(Note(midi=int(n), length_beats=note_length, velocity=velocity))
    return Track(name=name, notes=seq)
