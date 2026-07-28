"""
arccos_calculator.py

Deliverable 1 - Problem 4
SOEN 6011 - F1: arccos(x)

Implements arccos(x) using a Taylor/Maclaurin series expansion of arcsin(x),
via the identity: arccos(x) = pi/2 - arcsin(x)

Uses built-in math functions only for constants (math.pi) - the series
computation itself is done manually. (Full "from scratch" restriction
applies starting Deliverable 2.)
"""

import math

TOLERANCE = 1e-12
MAX_ITERATIONS = 1000


def _arcsin_series(x: float) -> float:
    """Core Taylor series summation, fast-converging for |x| <= ~0.7."""
    term = x
    total = x
    n = 1

    while abs(term) > TOLERANCE and n < MAX_ITERATIONS:
        term *= (x * x) * (2 * n - 1) / (2 * n)
        contribution = term / (2 * n + 1)
        total += contribution
        n += 1

    return total


def arcsin_taylor(x: float) -> float:
    """Compute arcsin(x) via Taylor series expansion.

    arcsin(x) = x + (1/6)x^3 + (3/40)x^5 + (15/336)x^7 + ...
    General term: nth_term = prev_nth_term * x^2 * (2n-1)/(2n), divided by (2n+1)

    NOTE: This series converges very slowly as |x| approaches 1 (it still
    converges mathematically, but needs an impractical number of terms to
    reach acceptable accuracy in floating-point). To keep the algorithm
    well-behaved across the full domain, values with |x| > 0.7 are computed
    via the complementary value sqrt(1 - x^2), where the series converges
    quickly, using arcsin(x) = sign(x) * (pi/2 - arcsin(sqrt(1-x^2))).
    """
    if x == 0:
        return 0.0

    if abs(x) > 0.7:
        y = math.sqrt(1 - x * x)
        return math.copysign(1, x) * ((math.pi / 2) - _arcsin_series(y))

    return _arcsin_series(x)


def arccos(x: float) -> float:
    """Compute arccos(x) in radians using the arcsin identity."""
    if x < -1 or x > 1:
        raise ValueError(f"x must be in [-1, 1], got {x}")
    return (math.pi / 2) - arcsin_taylor(x)


def main():
    print("=" * 50)
    print(" arccos(x) Calculator  |  F1: Deliverable 1")
    print("=" * 50)
    print("This tool computes arccos(x) in radians for x in [-1, 1].")
    print("Type 'q' at any time to quit.\n")

    while True:
        raw = input("Enter x (or 'q' to quit): ").strip()
        if raw.lower() == 'q':
            print("Goodbye.")
            break

        try:
            x = float(raw)
        except ValueError:
            print(f'  Error: "{raw}" is not a valid number. Please try again.\n')
            continue

        try:
            result = arccos(x)
            print(f"  arccos({x}) = {result:.6f} radians\n")
        except ValueError as e:
            print(f"  Error: {e}. Valid domain is [-1, 1]. Please try again.\n")


if __name__ == "__main__":
    main()
