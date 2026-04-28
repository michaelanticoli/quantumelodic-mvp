"""Tests for the Flask API endpoints (app.py).

Covers:
- /api/health
- /api/report   (free, no auth)
- /api/song-prompt (premium, requires premium_token)
"""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app as flask_app  # noqa: E402


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


SAMPLE_BIRTH = {
    "date": "1990-06-15",
    "time": "10:30",
    "lat": 34.0522,
    "lon": -118.2437,
    "timezone": "America/Los_Angeles",
}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


# ---------------------------------------------------------------------------
# /api/report – free endpoint
# ---------------------------------------------------------------------------
def test_report_returns_200(client):
    resp = client.post("/api/report", json=SAMPLE_BIRTH)
    assert resp.status_code == 200


def test_report_contains_expected_keys(client):
    data = client.post("/api/report", json=SAMPLE_BIRTH).get_json()
    for key in ("report", "harmonic", "sun_sign", "moon_sign", "rising_sign", "summary"):
        assert key in data, f"Missing key: {key}"


def test_report_planets_non_empty(client):
    data = client.post("/api/report", json=SAMPLE_BIRTH).get_json()
    planets = data["report"]["planets"]
    assert len(planets) > 0, "Planet list should not be empty"


def test_report_planets_have_sign(client):
    data = client.post("/api/report", json=SAMPLE_BIRTH).get_json()
    for p in data["report"]["planets"]:
        assert "sign" in p, f"Planet {p.get('name')} missing 'sign' field"
        assert p["sign"], f"Planet {p.get('name')} has empty 'sign'"


def test_report_aspects_present(client):
    data = client.post("/api/report", json=SAMPLE_BIRTH).get_json()
    # aspects list can be empty for some charts but key must exist
    assert "aspects" in data["report"]


def test_report_harmonic_fields(client):
    data = client.post("/api/report", json=SAMPLE_BIRTH).get_json()
    h = data["harmonic"]
    for key in ("primary_pentatonic_mode", "primary_quadratonic_mode",
                "harmonic_tension_index", "dominant_element", "sonic_payload"):
        assert key in h, f"Missing harmonic key: {key}"


def test_report_missing_field_returns_400(client):
    bad = {k: v for k, v in SAMPLE_BIRTH.items() if k != "timezone"}
    resp = client.post("/api/report", json=bad)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_report_no_account_required(client):
    """No authentication headers should be needed for the free report."""
    resp = client.post("/api/report", json=SAMPLE_BIRTH)
    # Must succeed without any Authorization header
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# /api/song-prompt – premium endpoint
# ---------------------------------------------------------------------------
def test_song_prompt_without_token_returns_402(client):
    resp = client.post("/api/song-prompt", json=SAMPLE_BIRTH)
    assert resp.status_code == 402
    assert "premium_token" in resp.get_json()["error"]


def test_song_prompt_with_empty_token_returns_402(client):
    payload = {**SAMPLE_BIRTH, "premium_token": ""}
    resp = client.post("/api/song-prompt", json=payload)
    assert resp.status_code == 402


def test_song_prompt_with_token_returns_200(client):
    payload = {**SAMPLE_BIRTH, "premium_token": "test-token-123"}
    resp = client.post("/api/song-prompt", json=payload)
    assert resp.status_code == 200


def test_song_prompt_contains_suno_prompt(client):
    payload = {**SAMPLE_BIRTH, "premium_token": "test-token-abc"}
    data = client.post("/api/song-prompt", json=payload).get_json()
    assert "suno_prompt" in data
    assert isinstance(data["suno_prompt"], str)
    assert len(data["suno_prompt"]) > 0


def test_song_prompt_contains_stable_audio_payload(client):
    payload = {**SAMPLE_BIRTH, "premium_token": "test-token-abc"}
    data = client.post("/api/song-prompt", json=payload).get_json()
    assert "stable_audio_payload" in data
    assert "title" in data["stable_audio_payload"]
