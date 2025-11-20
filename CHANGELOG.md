# CHANGELOG

All notable changes to this project are documented in this file.

For full release notes and historical entries (v1.0.0 → v1.3.0) see the Notion page:
https://www.notion.so/CHANGELOG-Quantumelodic-MVP-074f42eca2eb49309dba44422b34c171

## [1.3.0] - 2025-11-20
### Added
- Integrated canonical 24-mode cosmology into the harmonic engine.
- CSV-driven canonical mappings: pentatonic/quadratonic modes, modal families index, element timbres.
- Backward-compatible `load_map()` wrapper in `src/harmonic_engine/data_loader.py`.

### Changed
- Replaced harmonic engine stub with canonical-aware implementation.

### Tests
- Updated and verified unit tests; all tests passing locally (4/4).

## [Unreleased]
- Roadmap: v1.4.0 - MIDI Export; v1.5.0 - Hexatonic/Heptatonic support.
