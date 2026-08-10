# arccos(x) Calculator — F1

SOEN 6011: Software Engineering Processes — Section CC
Concordia University, Summer 2026

Implementation of the transcendental function **F1: arccos(x)**, developed
incrementally across Deliverables 1–3.

**Current version:** `1.1.3` (Semantic Versioning — see [Versioning](#versioning) below)

## Overview

This project implements the inverse cosine function `arccos(x)` in Python,
without relying on Python's built-in `math.acos()` (or any other library
math function, as of Deliverable 2). The core numerical method is a
Taylor series expansion of `arcsin(x)`, combined via the identity:

```
arccos(x) = π/2 − arcsin(x)
```

Deliverable 3 further hardens the implementation: PEP-8/Flake8 compliance,
a 10.00/10 Pylint score, documented debugger usage, Semantic Versioning,
User Interface Design Principles (UIDP) applied to the GUI, accessibility
improvements, and a full unit test suite.

## Files

| File | Description |
|---|---|
| `arccos_calculator.py` | Deliverable 1: textual UI, uses `math.pi`/`math.sqrt` |
| `arccos_scratch.py` | Deliverable 2/3: fully from-scratch core (π via Machin's formula, square root via Newton's method, custom `DomainError` exception, NaN/infinity handling) |
| `arccos_gui.py` | Deliverable 2/3: Tkinter GUI wrapping `arccos_scratch.py`, with UIDP-driven design and accessibility features |
| `test_arccos_scratch.py` | Deliverable 3: unit tests (PyUnit/`unittest`) for the core implementation |
| `test_arccos_gui.py` | Deliverable 3: unit tests for the GUI's calculation/display logic |

## Requirements

- Python 3.9+
- No external packages required (standard library only, including `tkinter`)
- Flake8 and Pylint (optional, for reproducing the code-quality checks below):
  ```bash
  python3 -m pip install flake8 pylint
  ```

### macOS note on Tkinter

If `import tkinter` fails with a `_tkinter` error, your Python installation
is likely missing Tk bindings. For Homebrew-installed Python:

```bash
brew install python-tk@3.13   # match your Python version
```

Then rebuild your virtual environment so it picks up the new binary.

## Usage

**Textual interface (Deliverable 1):**
```bash
python3 arccos_calculator.py
```

**From-scratch core, used directly (Deliverable 2/3):**
```python
from arccos_scratch import arccos_scratch
print(arccos_scratch(0.5))  # 1.0471975511965976
```

**GUI (Deliverable 2/3):**
```bash
python3 arccos_gui.py
```
Enter a value of `x` in `[-1, 1]` and click **Calculate**. A correct
result is shown in green with a ✓ symbol; invalid input (out-of-domain,
NaN, infinity, or non-numeric) is shown in red with a ✗ symbol and a
plain-language error message — color is never the only signal, per
WCAG 1.4.1 (Use of Color).

## Algorithm

`arccos(x)` is computed via a Taylor/Maclaurin series expansion of
`arcsin(x)`:

```
arcsin(x) = x + (1/6)x³ + (3/40)x⁵ + (15/336)x⁷ + ...
```

To avoid slow convergence near `x = ±1`, values with `|x| > 0.7` are
computed via the complementary-argument identity:

```
arcsin(x) = sign(x) · (π/2 − arcsin(√(1 − x²)))
```

which stays in the fast-converging region of the series regardless of
how close `x` is to the domain boundary.

Domain validation also rejects `NaN` (via the `x != x` self-comparison
identity, since `NaN` is the only float never equal to itself) and
infinite values, in addition to ordinary out-of-range input.

### From-scratch subordinate functions (Deliverable 2)

Deliverable 2 prohibits use of built-in/library math functions (aside
from arithmetic, input, output, and UI). The following were implemented
from scratch to support this:

- **π** — computed via Machin's formula, `π/4 = 4·arctan(1/5) − arctan(1/239)`,
  where `arctan` is itself computed via its own Taylor series.
- **Square root** — computed via Newton's method (Babylonian method).
- **Sign** — a simple hand-rolled sign function.

## Code Quality (Deliverable 3)

- **PEP-8 / Flake8:** `arccos_scratch.py` and `arccos_gui.py` are Flake8-clean.
  ```bash
  python3 -m flake8 arccos_scratch.py arccos_gui.py
  ```
- **Pylint:** both files score **10.00/10**.
  ```bash
  pylint arccos_scratch.py arccos_gui.py
  ```
- **Debugger (pdb):** used to step through `arcsin_scratch()`'s
  convergence-fix branch and through a unit test's assertion, inspecting
  intermediate values before trusting automated results.

## User Interface Design Principles (UIDP)

Eight candidate UIDP were evaluated via mind map against `arccos_gui.py`.
Six were judged to genuinely apply and are implemented directly:
Visibility of System Status, Consistency and Standards, Error Prevention,
Feedback, Recognition Rather Than Recall, and Aesthetic and Minimalist
Design. Two — Flexibility/Efficiency of Use and User Control/Freedom —
were judged only minimally applicable given the tool's intentionally
simple, single-purpose design. See inline comments in `arccos_gui.py`
for where each principle is applied.

## Accessibility

- Success/error state is signaled by **both** color and a checkmark/cross
  symbol, not color alone (WCAG 1.4.1: Use of Color), so colorblind users
  can distinguish outcomes without relying on hue.
- All interactive widgets (entry field, both buttons) are reachable via
  Tab in natural order; Return in the entry field triggers Calculate.
- Text sizing and dark-on-light contrast were chosen for legibility.

## Versioning

Source code follows [Semantic Versioning](https://semver.org)
(`MAJOR.MINOR.PATCH`), tracked via `__version__` in `arccos_scratch.py`
and as annotated Git tags:

| Version | Description |
|---|---|
| `1.0.0` | Initial from-scratch implementation with GUI and `DomainError` |
| `1.0.1` | Fix `DomainError` message duplication bug |
| `1.1.0` | Add NaN input validation |
| `1.1.1` | PEP-8 compliance fixes (Flake8 clean) |
| `1.1.2` | Pylint findings addressed (10.00/10) |
| `1.1.3` | Display version number in GUI title bar |

View the full tag history:
```bash
git tag -n
```

## Requirements Traceability

See the project's D1/D2 presentation slides for the full ISO/IEC/IEEE
29148-style requirements list (REQ-01 through REQ-10) and their mapping
to specific code sections, including requirements added/modified in
Deliverable 2 (GUI, custom exception, from-scratch constraint).

## Testing

**Correctness:** verified by comparing output against Python's built-in
`math.acos()` across the domain `[-1, 1]`, including boundary values
(`x = ±1`, `x = ±0.9999`), with observed error on the order of `10⁻¹³`
to `10⁻¹⁴`.

**Unit tests (Deliverable 3):** 35 unit tests using Python's built-in
`unittest` (PyUnit) framework, covering subordinate function correctness
(π, square root, sign), arccos correctness, domain validation
(out-of-range, NaN, infinity, empty/non-numeric input), and GUI
calculation logic.

```bash
python3 -m unittest discover -v
```

## Author

Vedant Nitinkumar Patel (Student ID: 40197890)
