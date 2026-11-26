# tests for the decay simulation
import numpy as np
import pytest
from decay import simulate


def test_starts_at_n0():
    # at time zero no atoms have decayed yet
    assert simulate(1000, 0.4)[0] == 1000


def test_rejects_negative_rate():
    # a negative decay rate makes no physical sense, so it must raise an error
    with pytest.raises(ValueError):
        simulate(1000, -0.1)


def test_matches_law():
    # average over many seeds should follow n0 * exp(-lam * t)
    n0, lam, dt, steps = 10000, 0.3, 0.05, 20
    t = steps * dt  # t = 1.0
    results = [simulate(n0, lam, dt=dt, steps=steps, seed=s)[-1] for s in range(50)]
    expected = n0 * np.exp(-lam * t)
    assert np.mean(results) == pytest.approx(expected, rel=0.02)
