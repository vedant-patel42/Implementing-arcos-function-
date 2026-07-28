"""
arccos_scratch.py

Deliverable 2 - Problem 5
SOEN 6011 - F1: arccos(x)

Subordinate functions implemented from scratch:
  - PI            : computed via Machin's formula
  - my_sqrt(x)    : computed via Newton's method (Babylonian method)
  - my_sign(x)    : sign of x, hand-rolled
  - arctan_series : Taylor series for arctan, used to compute PI
  - arcsin_taylor : Taylor series for arcsin (same technique as D1),
                    used to compute arccos via the identity
                    arccos(x) = PI/2 - arcsin(x)
"""

TOLERANCE = 1e-12
MAX_ITERATIONS = 1000


class DomainError(Exception):
    """Raised when x is outside the valid domain [-1, 1] for arccos(x)."""
 
    def __init__(self, x: float):
        self.x = x
        message = (
            f"x must be in [-1, 1], got {x}. "
            f"Please enter a value within the valid domain."
        )
        super().__init__(message)

# ----------------------------------------------------------------------
# Subordinate function 1: square root, via Newton's method
# ----------------------------------------------------------------------
def my_sqrt(x: float) -> float:
    """Compute sqrt(x) for x >= 0 using Newton's method (Babylonian method).

    Repeatedly refines a guess g using g_new = (g + x/g) / 2, which
    converges quadratically to sqrt(x).
    """
    if x < 0:
        raise ValueError(f"Cannot compute square root of negative number: {x}")
    if x == 0:
        return 0.0

    guess = x / 2 if x > 1 else 1.0  # reasonable starting guess
    for _ in range(MAX_ITERATIONS):
        next_guess = (guess + x / guess) / 2
        if abs(next_guess - guess) < TOLERANCE:
            return next_guess
        guess = next_guess
    return guess


# ----------------------------------------------------------------------
# Subordinate function 2: sign, hand-rolled
# ----------------------------------------------------------------------
def my_sign(x: float) -> float:
    """Return 1.0 if x >= 0, else -1.0 (hand-rolled replacement for
    math.copysign's sign-extraction behavior as used in D1)."""
    return 1.0 if x >= 0 else -1.0


# ----------------------------------------------------------------------
# Subordinate function 3: arctan, via Taylor series
# ----------------------------------------------------------------------
def _arctan_series(x: float) -> float:
    """Taylor series for arctan(x), valid/fast-converging for |x| <= 1.

    arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
    """
    term = x
    total = x
    x_squared = x * x
    n = 1

    while abs(term) > TOLERANCE and n < MAX_ITERATIONS:
        term *= -x_squared
        contribution = term / (2 * n + 1)
        total += contribution
        n += 1

    return total


# ----------------------------------------------------------------------
# Subordinate function 4: PI, via Machin's formula
# ----------------------------------------------------------------------
def _compute_pi() -> float:
    """Compute PI from scratch using Machin's formula:

        pi/4 = 4*arctan(1/5) - arctan(1/239)
    """
    return 4 * (4 * _arctan_series(1 / 5) - _arctan_series(1 / 239))


PI = _compute_pi()


# ----------------------------------------------------------------------
# arcsin via Taylor series (same technique as D1), now built entirely
# on the from-scratch primitives above
# ----------------------------------------------------------------------
def _arcsin_series(x: float) -> float:
    """Core Taylor series summation for arcsin, fast-converging for
    |x| <= ~0.7."""
    term = x
    total = x
    n = 1

    while abs(term) > TOLERANCE and n < MAX_ITERATIONS:
        term *= (x * x) * (2 * n - 1) / (2 * n)
        contribution = term / (2 * n + 1)
        total += contribution
        n += 1

    return total


def arcsin_scratch(x: float) -> float:
    """Compute arcsin(x) using the Taylor series, with the same
    complementary-argument reduction used in D1 for |x| > 0.7, now using
    my_sqrt and my_sign instead of math.sqrt/math.copysign."""
    if x == 0:
        return 0.0

    if abs(x) > 0.7:
        y = my_sqrt(1 - x * x)
        return my_sign(x) * (PI / 2 - _arcsin_series(y))

    return _arcsin_series(x)


def arccos_scratch(x: float) -> float:
    """Compute arccos(x) in radians, fully from scratch."""
    if x < -1 or x > 1:
        raise ValueError(f"x must be in [-1, 1], got {x}")
    return (PI / 2) - arcsin_scratch(x)