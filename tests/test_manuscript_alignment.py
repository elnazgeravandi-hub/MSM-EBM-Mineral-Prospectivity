from pathlib import Path
import yaml
from src.schema import FEATURES
from src.fuzzy import small
from src.models import ebm_raw, msm_ebm

def test_documented_chronology_matches_revised_manuscript():
    for path in (Path('README.md'), Path('docs/SCIENTIFIC_LIMITATIONS.md')):
        content = path.read_text().lower()
        assert 'sampling radius was informed by nna' not in content
        assert 'a priori' in content

def test_model_and_geo_configuration_reference():
    cfg = yaml.safe_load(Path('configs/manuscript.yaml').read_text())
    assert len(FEATURES) == 12 and len(set(FEATURES)) == 12
    assert cfg['reference_block_m'] == 6000
    assert cfg['reference_buffer_m'] == 900
    assert cfg['models']['ebm']['interactions'] == 0
    assert abs(float(small([1500])[0]) - .5) < 1e-12
