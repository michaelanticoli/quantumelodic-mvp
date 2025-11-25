"""Prompt builder for AI music generation from harmonic analysis."""

import json
from typing import Dict, Any, List

from .style_mappings import (
    MODAL_STYLES,
    ELEMENT_DESCRIPTIONS,
    PLANET_INSTRUMENTS,
    tension_to_dynamics,
    modal_to_genre_tags,
)


class MusicPromptBuilder:
    """Generate AI music prompts from Quantumelodic harmonic analysis."""
    
    def __init__(self, result):
        """Initialize with harmonic engine output."""
        self.result = result
    
    def _create_title(self) -> str:
        """Generate track title."""
        mode = self.result.primary_pentatonic_mode
        element = self.result.dominant_element
        return f"{mode} - {element} piece"
    
    def _create_description(self) -> str:
        """Generate the core musical description."""
        modal_style = MODAL_STYLES.get(self.result.primary_pentatonic_mode, '')
        element_desc = ELEMENT_DESCRIPTIONS.get(self.result.dominant_element, '')
        sonic = self.result.sonic_payload
        
        return (
            f"A {modal_style}. "
            f"Texture: {element_desc}. "
            f"Recommended tempo: {sonic.recommended_tempo_bpm} BPM. "
            f"Waveform character: {sonic.waveform}."
        )
    
    def _create_tags(self) -> List[str]:
        """Generate genre/mood tags."""
        tags = modal_to_genre_tags(self.result.primary_pentatonic_mode)
        tags.append(self.result.dominant_element.lower())
        tags.append(f"hti-{self.result.harmonic_tension_index}")
        return tags
    
    def _create_lyrics(self) -> str:
        """Generate thematic lyrical direction."""
        element = self.result.dominant_element
        mood = 'calm' if self.result.harmonic_tension_index < 40 else 'urgent'
        return f"A {mood} meditation on {element.lower()}, soundscapes and inner motion."
    
    def _get_structure_description(self) -> str:
        """Generate structural/arrangement description."""
        tense = self.result.harmonic_tension_index
        if tense < 30:
            return 'ambient intro -> gentle theme -> ambient outro'
        if tense < 60:
            return 'intro -> build -> motif -> bridge -> resolution'
        return 'strong intro -> driving section -> intense climax -> release'
    
    def build_suno_prompt(self) -> str:
        """Build a single-string prompt for Suno-style generation."""
        title = self._create_title()
        desc = self._create_description()
        tags = ', '.join(self._create_tags())
        structure = self._get_structure_description()
        return f"Title: {title}\nDescription: {desc}\nStructure: {structure}\nTags: {tags}"
    
    def build_stable_audio_prompt(self) -> Dict[str, Any]:
        """Build a structured prompt payload for Stable Audio."""
        payload = {
            'title': self._create_title(),
            'description': self._create_description(),
            'tags': self._create_tags(),
            'lyrics': self._create_lyrics(),
            'structure': self._get_structure_description(),
            'dynamics': tension_to_dynamics(self.result.harmonic_tension_index),
            'instruments': self._get_instrument_suggestions(),
            'tempo_bpm': self.result.sonic_payload.recommended_tempo_bpm,
        }
        return payload
    
    def _get_instrument_suggestions(self) -> List[str]:
        """Generate instrument suggestions based on element."""
        instruments = []
        elem = self.result.dominant_element
        
        if elem == 'Fire':
            instruments.extend(PLANET_INSTRUMENTS.get('Mars', []))
            instruments.extend(PLANET_INSTRUMENTS.get('Sun', []))
        elif elem == 'Water':
            instruments.extend(PLANET_INSTRUMENTS.get('Moon', []))
            instruments.extend(PLANET_INSTRUMENTS.get('Neptune', []))
        elif elem == 'Air':
            instruments.extend(PLANET_INSTRUMENTS.get('Mercury', []))
            instruments.extend(PLANET_INSTRUMENTS.get('Uranus', []))
        elif elem == 'Earth':
            instruments.extend(PLANET_INSTRUMENTS.get('Venus', []))
            instruments.extend(PLANET_INSTRUMENTS.get('Saturn', []))
        
        # Remove duplicates
        out = []
        for i in instruments:
            if i not in out:
                out.append(i)
        return out[:6]
    
    def export_to_json(self, path: str) -> str:
        """Export prompt to JSON file."""
        payload = self.build_stable_audio_prompt()
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2)
        return path