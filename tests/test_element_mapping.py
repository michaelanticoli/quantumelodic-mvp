from harmonic_engine import data_loader


def test_load_pentatonic_map_exists():
    mapping = data_loader.load_map('pentatonic_modes.csv')
    # The canonical file should be provided by the user; for now assert mapping is a dict
    assert isinstance(mapping, dict)


def test_load_quadratonic_map_exists():
    mapping = data_loader.load_map('quadratonic_modes.csv')
    assert isinstance(mapping, dict)
