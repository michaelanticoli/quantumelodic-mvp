# Quantumelodic MVP

Quantumelodic MVP - Astronomical Music Generation

## Overview

This project translates astronomical phenomena into musical compositions using quantum-inspired algorithms. It combines Python-based astronomical calculations with a modern web frontend.

## Components

### Backend (Python)
- **Ephemeris Engine**: Calculate astronomical positions and events using skyfield
- **Harmonic Engine**: Map celestial data to musical harmony with canonical 24-mode cosmology
- **MIDI Engine**: Generate playable MIDI compositions
- **AI Music Engine**: Intelligent music pattern generation

### Frontend (Vue.js + Vite)
A modern web interface for interacting with the Quantumelodic system.

## Getting Started

### Prerequisites
- Python 3.x
- Node.js 20.x or higher
- npm

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000/

3. Build for production:
```bash
npm run build
```

## Development

- Frontend source code is in `quantumelodic-frontend/`
- Python backend modules are in `src/`
- Examples and demos are in `examples/`

## Testing

Run Python tests:
```bash
pytest
```

## Version

Current version: v1.3.0

See [CHANGELOG.md](CHANGELOG.md) for version history and [VERSION](VERSION) for release notes.

## License

ISC
