"""
arccos_gui.py

Deliverable 2 - Problem 5
SOEN 6011 - F1: arccos(x)

Tkinter graphical user interface wrapping the from-scratch arccos
implementation in arccos_scratch.py. No built-in/library math functions
are used for the computation itself; Tkinter is used only for the UI,
which is explicitly permitted by the D2 "from scratch" constraint.
"""

import tkinter as tk
from tkinter import ttk

from arccos_scratch import arccos_scratch, DomainError


class ArccosApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("arccos(x) Calculator — F1, Deliverable 2")
        self.root.geometry("420x260")
        self.root.resizable(False, False)

        self._build_widgets()

    def _build_widgets(self):
        padding = {"padx": 12, "pady": 6}

        title_label = ttk.Label(
            self.root,
            text="arccos(x) Calculator",
            font=("Helvetica", 16, "bold"),
        )
        title_label.pack(pady=(16, 4))

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
        self.result_label.configure(foreground="#1a7f37")  # green
        self.result_var.set(text)

    def _show_error(self, text: str):
        self.result_label.configure(foreground="#c92a2a")  # red
        self.result_var.set(f"Error: {text}")


def main():
    root = tk.Tk()
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    ArccosApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
