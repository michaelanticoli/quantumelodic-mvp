"""Quantumelodic MVP – Flask API server.

Endpoints
---------
POST /api/report          – Free: generate the Quantumelodic natal-chart report.
POST /api/song-prompt     – Premium: return AI-music prompt data (requires
                            a valid ``premium_token`` in the JSON body; in
                            production replace this check with a real Stripe
                            webhook / session-verified token).
GET  /api/health          – Simple health-check / readiness probe.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Path setup so the src/ packages are importable regardless of working dir
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from ephemeris_engine.chart_builder import build_chart_from_birth_data  # noqa: E402
from harmonic_engine.engine import run_harmonic_engine                   # noqa: E402
from reporting.report import generate_report                             # noqa: E402
from ai_music_engine.prompt_builder import MusicPromptBuilder            # noqa: E402

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Free endpoint – natal chart report
# ---------------------------------------------------------------------------
@app.post("/api/report")
def report():
    """Return the free Quantumelodic report for the supplied birth data.

    Expected JSON body::

        {
            "date":     "YYYY-MM-DD",
            "time":     "HH:MM",
            "lat":      <float>,
            "lon":      <float>,
            "timezone": "<IANA timezone string>"
        }
    """
    body = request.get_json(silent=True) or {}

    required = ("date", "time", "lat", "lon", "timezone")
    missing = [k for k in required if k not in body]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        chart = build_chart_from_birth_data(
            date=str(body["date"]),
            time=str(body["time"]),
            location_lat=float(body["lat"]),
            location_lon=float(body["lon"]),
            timezone=str(body["timezone"]),
        )
        engine_result = run_harmonic_engine(chart)
        rep = generate_report(chart, engine_result)
    except Exception:  # pragma: no cover
        return jsonify({"error": "Failed to generate report. Please check your input values."}), 422

    return jsonify(
        {
            "report": rep["json"],
            "summary": rep["text"],
            "harmonic": {
                "primary_pentatonic_mode": engine_result.primary_pentatonic_mode,
                "primary_quadratonic_mode": engine_result.primary_quadratonic_mode,
                "harmonic_tension_index": engine_result.harmonic_tension_index,
                "dominant_element": engine_result.dominant_element,
                "sonic_payload": {
                    "waveform": engine_result.sonic_payload.waveform,
                    "recommended_tempo_bpm": engine_result.sonic_payload.recommended_tempo_bpm,
                    "timbres": engine_result.sonic_payload.timbres,
                },
            },
            "sun_sign": chart.sun_sign,
            "moon_sign": chart.moon_sign,
            "rising_sign": chart.rising_sign,
        }
    )


# ---------------------------------------------------------------------------
# Premium endpoint – AI music prompt
# ---------------------------------------------------------------------------
@app.post("/api/song-prompt")
def song_prompt():
    """Return a premium AI-music prompt for the supplied birth data.

    In addition to the birth-data fields required by /api/report the body
    must include ``premium_token``.  In a production deployment replace the
    token check below with a real Stripe session/webhook verification.

    Expected JSON body::

        {
            "date":          "YYYY-MM-DD",
            "time":          "HH:MM",
            "lat":           <float>,
            "lon":           <float>,
            "timezone":      "<IANA timezone string>",
            "premium_token": "<stripe-session-id or verified token>"
        }
    """
    body = request.get_json(silent=True) or {}

    # --- token check (swap for real Stripe verification in production) ---
    token = body.get("premium_token", "").strip()
    if not token:
        return jsonify({"error": "premium_token is required"}), 402

    required = ("date", "time", "lat", "lon", "timezone")
    missing = [k for k in required if k not in body]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        chart = build_chart_from_birth_data(
            date=str(body["date"]),
            time=str(body["time"]),
            location_lat=float(body["lat"]),
            location_lon=float(body["lon"]),
            timezone=str(body["timezone"]),
        )
        engine_result = run_harmonic_engine(chart)
        builder = MusicPromptBuilder(engine_result)
        suno_prompt = builder.build_suno_prompt()
        stable_payload = builder.build_stable_audio_prompt()
    except Exception:  # pragma: no cover
        return jsonify({"error": "Failed to generate song prompt. Please check your input values."}), 422

    return jsonify(
        {
            "suno_prompt": suno_prompt,
            "stable_audio_payload": stable_payload,
            "dominant_element": engine_result.dominant_element,
            "harmonic_tension_index": engine_result.harmonic_tension_index,
        }
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0").strip() == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
