"""
test_arccos_gui.py

Deliverable 3 - Problem 8
SOEN 6011 - F1: arccos(x)

Unit tests for the GUI's internal logic (input parsing, domain
validation, and result/error formatting), using Python's built-in
unittest framework (PyUnit).

These tests exercise ArccosApp's calculation logic directly rather
than driving the Tkinter event loop, since GUI event simulation is
inherently environment-dependent (requires a display); testing the
underlying logic is both more reliable and closer to standard unit
testing practice.

Run with:
    python3 -m unittest test_arccos_gui.py -v
"""

import unittest
import tkinter as tk

from arccos_gui import ArccosApp


def _tk_available() -> bool:
    """Check whether a Tk display is available in this environment."""
    try:
        root = tk.Tk()
        root.destroy()
        return True
    except tk.TclError:
        return False


@unittest.skipUnless(_tk_available(), "No display available for Tkinter")
class TestArccosAppCalculation(unittest.TestCase):
    """Tests for ArccosApp's _on_calculate logic."""

    def setUp(self):
        self.root = tk.Tk()
        self.app = ArccosApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def _enter_and_calculate(self, text: str) -> str:
        self.app.x_entry.delete(0, tk.END)
        self.app.x_entry.insert(0, text)
        self.app._on_calculate()  # pylint: disable=protected-access
        return self.app.result_var.get()

    def test_valid_input_shows_checkmark_and_result(self):
        result = self._enter_and_calculate("0.5")
        self.assertTrue(result.startswith("\u2713"))
        self.assertIn("radians", result)
        self.assertIn("1.047198", result)

    def test_out_of_domain_shows_cross_and_error(self):
        result = self._enter_and_calculate("2")
        self.assertTrue(result.startswith("\u2717"))
        self.assertIn("Error", result)
        self.assertIn("[-1, 1]", result)

    def test_non_numeric_shows_cross_and_error(self):
        result = self._enter_and_calculate("abc")
        self.assertTrue(result.startswith("\u2717"))
        self.assertIn("not a valid number", result)

    def test_empty_input_shows_cross_and_error(self):
        result = self._enter_and_calculate("")
        self.assertTrue(result.startswith("\u2717"))
        self.assertIn("not a valid number", result)

    def test_clear_resets_result(self):
        self._enter_and_calculate("0.5")
        self.app._on_clear()  # pylint: disable=protected-access
        self.assertEqual(self.app.result_var.get(), "")
        self.assertEqual(self.app.x_entry.get(), "")

    def test_boundary_value_one(self):
        result = self._enter_and_calculate("1")
        self.assertTrue(result.startswith("\u2713"))
        self.assertIn("0.000000", result)

    def test_boundary_value_negative_one(self):
        result = self._enter_and_calculate("-1")
        self.assertTrue(result.startswith("\u2713"))
        self.assertIn("3.141593", result)


if __name__ == "__main__":
    unittest.main()
