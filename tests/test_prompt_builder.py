import json
import types
import pytest

from ai_music_engine.prompt_builder import MusicPromptBuilder
from ai_music_engine.style_mappings import MODAL_STYLES

def make_mock_result():
    """Creates a simple mock HarmonicResult object for testing."""
    sonic_payload = types.SimpleNamespace(
        recommended_tempo_bpm=120,
        waveform='sine'
    )
    result = types.SimpleNamespace(
        primary_pentatonic_mode='PENT-TEST-1',
        dominant_element='Air',
        harmonic_tension_index=50,
        sonic_payload=sonic_payload
    )
    return result


def test_builder_initializes():
    """Verify MusicPromptBuilder(result) works."""
    result = make_mock_result()
    builder = MusicPromptBuilder(result)
    assert isinstance(builder, MusicPromptBuilder)
    assert builder.result == result


def test_stable_audio_has_title():
    """Verify build_stable_audio_prompt() returns dict with 'title' key."""
    result = make_mock_result()
    builder = MusicPromptBuilder(result)
    prompt = builder.build_stable_audio_prompt()
    assert isinstance(prompt, dict)
    assert 'title' in prompt


def test_suno_prompt_is_string():
    """Verify build_suno_prompt() returns a string."""
    result = make_mock_result()
    builder = MusicPromptBuilder(result)
    prompt = builder.build_suno_prompt()
    assert isinstance(prompt, str)


def test_all_modal_styles_generate_prompts():
    """Iterate all keys in MODAL_STYLES, verify each generates a non-empty description in the payload."""
    for mode_id in MODAL_STYLES.keys():
        result = make_mock_result()
        result.primary_pentatonic_mode = mode_id

        builder = MusicPromptBuilder(result)
        prompt = builder.build_stable_audio_prompt()

        assert 'description' in prompt
        assert prompt['description']


def test_export_to_json(tmp_path):
    """Use tmp_path fixture, call export_to_json, verify file exists and contains valid JSON with title, description, tags keys."""
    result = make_mock_result()
    builder = MusicPromptBuilder(result)
    out_file = tmp_path / "prompt.json"

    builder.export_to_json(str(out_file))

    assert out_file.exists()
    with open(out_file, 'r') as f:
        data = json.load(f)
    assert 'title' in data
    assert 'description' in data
    assert 'tags' in data