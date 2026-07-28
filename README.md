# arccos(x) Calculator — F1

SOEN 6011: Software Engineering Processes — Section CC
Concordia University, Summer 2026

Implementation of the transcendental function **F1: arccos(x)**, developed
incrementally across Deliverables 1–3.

## Overview

This project implements the inverse cosine function `arccos(x)` in Python,
without relying on Python's built-in `math.acos()` (or any other library
math function, as of Deliverable 2). The core numerical method is a
Taylor series expansion of `arcsin(x)`, combined via the identity:

```
arccos(x) = π/2 − arcsin(x)
```

## Files

| File | Description |
|---|---|
| `arccos_calculator.py` | Deliverable 1: textual UI, uses `math.pi`/`math.sqrt` |
| `arccos_scratch.py` | Deliverable 2: fully from-scratch core (π via Machin's formula, square root via Newton's method, custom `DomainError` exception) |
| `arccos_gui.py` | Deliverable 2: Tkinter GUI wrapping `arccos_scratch.py` |

## Requirements

- Python 3.9+
- No external packages required (standard library only, including `tkinter`)

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

**From-scratch core, used directly (Deliverable 2):**
```python
from arccos_scratch import arccos_scratch
print(arccos_scratch(0.5))  # 1.0471975511965976
```

**GUI (Deliverable 2):**
```bash
python3 arccos_gui.py
```
Enter a value of `x` in `[-1, 1]` and click **Calculate**. The result is
shown in radians; invalid input (out-of-domain or non-numeric) is shown
as a clear, in-window error message rather than crashing the program.

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

### From-scratch subordinate functions (Deliverable 2)

Deliverable 2 prohibits use of built-in/library math functions (aside
from arithmetic, input, output, and UI). The following were implemented
from scratch to support this:

- **π** — computed via Machin's formula, `π/4 = 4·arctan(1/5) − arctan(1/239)`,
  where `arctan` is itself computed via its own Taylor series.
- **Square root** — computed via Newton's method (Babylonian method).
- **Sign** — a simple hand-rolled sign function.

## Requirements Traceability

See the project's D1/D2 presentation slides for the full ISO/IEC/IEEE
29148-style requirements list (REQ-01 through REQ-07) and their mapping
to specific code sections.

## Testing

Correctness was verified by comparing output against Python's built-in
`math.acos()` across the domain `[-1, 1]`, including boundary values
(`x = ±1`, `x = ±0.9999`), with observed error on the order of `10⁻¹³`
to `10⁻¹⁴`.

## Author

Vedant Nitinkumar Patel (Student ID: 40197890)
