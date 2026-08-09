"""
test_arccos_scratch.py

Deliverable 3 - Problem 8
SOEN 6011 - F1: arccos(x)

Unit tests for the from-scratch arccos implementation, using Python's
built-in unittest framework (PyUnit).

Run with:
    python3 -m unittest test_arccos_scratch.py -v
"""

import math
import unittest

from arccos_scratch import (
    arccos_scratch,
    arcsin_scratch,
    my_sqrt,
    my_sign,
    DomainError,
    PI,
)

TOLERANCE = 1e-9


class TestPiComputation(unittest.TestCase):
    """Tests for the from-scratch PI constant (Machin's formula)."""

    def test_pi_matches_reference(self):
        """Computed PI should closely match math.pi."""
        self.assertAlmostEqual(PI, math.pi, delta=TOLERANCE)


class TestMySqrt(unittest.TestCase):
    """Tests for the from-scratch square root (Newton's method)."""

    def test_perfect_square(self):
        self.assertAlmostEqual(my_sqrt(4), 2.0, delta=TOLERANCE)

    def test_non_perfect_square(self):
        self.assertAlmostEqual(my_sqrt(2), math.sqrt(2), delta=TOLERANCE)

    def test_zero(self):
        self.assertEqual(my_sqrt(0), 0.0)

    def test_small_value(self):
        self.assertAlmostEqual(my_sqrt(0.25), 0.5, delta=TOLERANCE)

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            my_sqrt(-1)


class TestMySign(unittest.TestCase):
    """Tests for the hand-rolled sign function."""

    def test_positive(self):
        self.assertEqual(my_sign(5), 1.0)

    def test_negative(self):
        self.assertEqual(my_sign(-5), -1.0)

    def test_zero_is_positive(self):
        # By convention in this implementation, 0 is treated as
        # non-negative (matches math.copysign(1, 0) behavior for +0.0).
        self.assertEqual(my_sign(0), 1.0)


class TestArcsinScratch(unittest.TestCase):
    """Tests for the from-scratch arcsin (used internally by arccos)."""

    def test_zero(self):
        self.assertEqual(arcsin_scratch(0), 0.0)

    def test_small_value_direct_series(self):
        # |x| <= 0.7 uses the direct series branch.
        self.assertAlmostEqual(
            arcsin_scratch(0.5), math.asin(0.5), delta=TOLERANCE
        )

    def test_large_value_uses_reduction(self):
        # |x| > 0.7 uses the complementary-argument reduction branch.
        self.assertAlmostEqual(
            arcsin_scratch(0.9), math.asin(0.9), delta=TOLERANCE
        )

    def test_negative_large_value(self):
        self.assertAlmostEqual(
            arcsin_scratch(-0.9), math.asin(-0.9), delta=TOLERANCE
        )


class TestArccosScratchCorrectness(unittest.TestCase):
    """Correctness tests: arccos_scratch(x) vs. math.acos(x)."""

    def test_standard_value(self):
        self.assertAlmostEqual(
            arccos_scratch(0.5), math.acos(0.5), delta=TOLERANCE
        )

    def test_zero(self):
        self.assertAlmostEqual(
            arccos_scratch(0), math.acos(0), delta=TOLERANCE
        )

    def test_negative_value(self):
        self.assertAlmostEqual(
            arccos_scratch(-0.3), math.acos(-0.3), delta=TOLERANCE
        )

    def test_boundary_positive_one(self):
        self.assertAlmostEqual(
            arccos_scratch(1), math.acos(1), delta=TOLERANCE
        )

    def test_boundary_negative_one(self):
        self.assertAlmostEqual(
            arccos_scratch(-1), math.acos(-1), delta=TOLERANCE
        )

    def test_near_boundary_positive(self):
        # Exercises the convergence-fix branch (|x| > 0.7).
        self.assertAlmostEqual(
            arccos_scratch(0.9999), math.acos(0.9999), delta=TOLERANCE
        )

    def test_near_boundary_negative(self):
        self.assertAlmostEqual(
            arccos_scratch(-0.9999), math.acos(-0.9999), delta=TOLERANCE
        )

    def test_result_in_valid_range(self):
        # arccos(x) must always be in [0, pi] for valid x.
        for x in (-1, -0.5, 0, 0.5, 1):
            result = arccos_scratch(x)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, PI)


class TestArccosScratchDomainValidation(unittest.TestCase):
    """Domain validation / exception tests."""

    def test_above_domain_raises_domain_error(self):
        with self.assertRaises(DomainError):
            arccos_scratch(2)

    def test_below_domain_raises_domain_error(self):
        with self.assertRaises(DomainError):
            arccos_scratch(-5)

    def test_slightly_above_domain_raises(self):
        with self.assertRaises(DomainError):
            arccos_scratch(1.0001)

    def test_nan_raises_domain_error(self):
        with self.assertRaises(DomainError):
            arccos_scratch(float("nan"))

    def test_positive_infinity_raises_domain_error(self):
        with self.assertRaises(DomainError):
            arccos_scratch(float("inf"))

    def test_negative_infinity_raises_domain_error(self):
        with self.assertRaises(DomainError):
            arccos_scratch(float("-inf"))

    def test_domain_error_message_contains_value(self):
        try:
            arccos_scratch(5)
            self.fail("Expected DomainError was not raised")
        except DomainError as e:
            self.assertIn("5", str(e))
            self.assertIn("[-1, 1]", str(e))


if __name__ == "__main__":
    unittest.main()
