"""
무리수-대수학 엔진 테스트.
"""

import math
import sys
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from cognitive_kernel.engines.irrational_algebra import IrrationalAlgebraEngine


def test_phi_sequence_prefers_phi():
    engine = IrrationalAlgebraEngine()
    snapshot = engine.analyze([1.0, 1.61803398875, 2.61803398875])

    assert snapshot.dominant_constant == "phi"
    assert snapshot.resonance_score > 0.9


def test_sqrt2_invariant_detected():
    engine = IrrationalAlgebraEngine()
    snapshot = engine.analyze([1.0, math.sqrt(2.0)])

    names = {inv.name for inv in snapshot.invariants}
    assert "sqrt2_quadratic" in names


def test_boundary_mismatch_penalizes_alignment():
    engine = IrrationalAlgebraEngine()
    good = engine.analyze([1.0, math.pi], boundary_mismatch=0.01)
    bad = engine.analyze([1.0, math.pi], boundary_mismatch=10.0)

    assert good.boundary_alignment > bad.boundary_alignment
    assert good.structural_health > bad.structural_health
