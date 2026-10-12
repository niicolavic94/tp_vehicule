"""Tests automatisés du module test_exemple."""


def test_exemple():
    """Vérifie le comportement attendu."""
    a = 5
    b = 6
    result_theory = 30
    result = a * b
    assert result == result_theory
