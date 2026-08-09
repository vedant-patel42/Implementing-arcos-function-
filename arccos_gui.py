"""
arccos_gui.py

Deliverable 2 - Problem 5 / Deliverable 3 - Problem 7
SOEN 6011 - F1: arccos(x)

Tkinter graphical user interface wrapping the from-scratch arccos
implementation in arccos_scratch.py. No built-in/library math functions
are used for the computation itself; Tkinter is used only for the UI,
which is explicitly permitted by the D2 "from scratch" constraint.

Versioning follows Semantic Versioning; see arccos_scratch.__version__
for the current version and version history.

User Interface Design Principles (UIDP) applied, per D3 mind map:
  - Visibility of System Status  (see _show_result / _show_error)
  - Consistency and Standards    (see _build_widgets: ttk throughout)
  - Error Prevention             (see domain_label)
  - Feedback                     (see _show_result / _show_error)
  - Recognition Rather Than Recall (see domain_label)
  - Aesthetic and Minimalist Design (see _build_widgets: 8 widgets total)
Flexibility/Efficiency of Use and User Control/Freedom were considered
and judged only minimally applicable given this tool's intentionally
simple, single-purpose, stateless design (see D3 mind map).

Accessibility (D3, Problem 7):
  - Keyboard operable: Entry accepts Return to trigger Calculate; all
    interactive widgets (entry, both buttons) are reachable via Tab in
    natural creation order (standard ttk focus traversal).
  - Color is never the sole signal: success/error state in the result
    label is conveyed by a checkmark/cross symbol in addition to color
    (WCAG 1.4.1: Use of Color), so colorblind users can distinguish
    outcomes without relying on hue.
  - Text sizing (10-16px) and dark-on-light contrast were chosen for
    legibility rather than purely aesthetic reasons.
"""

import tkinter as tk
from tkinter import ttk

from arccos_scratch import arccos_scratch, DomainError, __version__


class ArccosApp:  # pylint: disable=too-few-public-methods
    """Tkinter application wrapping arccos_scratch for interactive use.

    Structured as a class (rather than free functions) to group the
    widgets and their event handlers together; most of its methods are
    intentionally private (prefixed with _) since they are internal
    event callbacks, not a public API meant to be reused elsewhere.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"arccos(x) Calculator — F1, v{__version__}")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self._build_widgets()

    def _build_widgets(self):
        # UIDP - Aesthetic and Minimalist Design: 8 widgets total (3
        # interactive: entry + 2 buttons; 4 informational labels; 1
        # layout frame) -- no menus, tabs, settings, or scrollbars.
        # UIDP - Consistency and Standards: every widget below uses the
        # ttk (themed Tk) widget set, giving native OS look-and-feel
        # and consistent styling across all buttons/labels/entries.
        padding = {"padx": 12, "pady": 6}

        title_label = ttk.Label(
            self.root,
            text="arccos(x) Calculator",
            font=("Helvetica", 16, "bold"),
        )
        title_label.pack(pady=(16, 4))

        # UIDP - Error Prevention / Recognition Rather Than Recall: the
        # valid domain is shown before the user types anything, so they
        # never have to guess or remember the constraint.
        domain_label = ttk.Label(
            self.root,
            text="Enter a value of x in the range [-1, 1]",
            font=("Helvetica", 10),
            foreground="#444444",
        )
        domain_label.pack(pady=(0, 10))

        input_frame = ttk.Frame(self.root)
        input_frame.pack(**padding)

        x_label = ttk.Label(input_frame, text="x =")
        x_label.grid(row=0, column=0, padx=(0, 8))

        self.x_entry = ttk.Entry(input_frame, width=20)
        self.x_entry.grid(row=0, column=1)
        self.x_entry.bind("<Return>", lambda event: self._on_calculate())
        self.x_entry.focus()

        calculate_button = ttk.Button(
            self.root, text="Calculate", command=self._on_calculate
        )
        calculate_button.pack(pady=10)

        self.result_var = tk.StringVar(value="")
        self.result_label = ttk.Label(
            self.root,
            textvariable=self.result_var,
            font=("Helvetica", 12),
            wraplength=380,
            justify="center",
        )
        self.result_label.pack(pady=(6, 4))

        clear_button = ttk.Button(
            self.root, text="Clear", command=self._on_clear
        )
        clear_button.pack(pady=(4, 10))

    def _on_calculate(self):
        raw_text = self.x_entry.get().strip()

        # REQ-07 equivalent: handle non-numeric input gracefully.
        try:
            x = float(raw_text)
        except ValueError:
            self._show_error(
                f'"{raw_text}" is not a valid number. '
                f"Please enter a numeric value, e.g. 0.5."
            )
            return

        # REQ-02/REQ-03 equivalent: domain validation with a clear error.
        try:
            result = arccos_scratch(x)
        except DomainError as e:
            self._show_error(str(e))
            return

        # REQ-04/REQ-05 equivalent: labeled result in radians.
        self._show_result(f"arccos({x}) = {result:.6f} radians")

    def _on_clear(self):
        self.x_entry.delete(0, tk.END)
        self.result_var.set("")
        self.result_label.configure(foreground="black")
        self.x_entry.focus()

    def _show_result(self, text: str):
        # UIDP - Visibility of System Status / Feedback: every Calculate
        # click produces an immediate, visible response.
        # Accessibility: success is signaled by both color (green) AND
        # a leading checkmark symbol, not color alone, so the outcome
        # is distinguishable for colorblind users (WCAG 1.4.1: Use of
        # Color).
        self.result_label.configure(foreground="#1a7f37")  # green
        self.result_var.set(f"\u2713 {text}")

    def _show_error(self, text: str):
        # UIDP - Visibility of System Status / Feedback: errors are
        # shown in the same location as results, so failure is
        # immediately and unambiguously visible in-window (never a
        # silent failure or a console-only message).
        # Accessibility: failure is signaled by both color (red) AND a
        # leading cross symbol, not color alone, so the outcome is
        # distinguishable for colorblind users (WCAG 1.4.1: Use of
        # Color).
        self.result_label.configure(foreground="#c92a2a")  # red
        self.result_var.set(f"\u2717 Error: {text}")


def main():
    """Launch the arccos(x) calculator GUI."""
    root = tk.Tk()
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    ArccosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
