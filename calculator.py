"""GUI Calculator — a Tkinter version of my command-line calculator from the Python course.

The original asked for two numbers and an operator in the terminal and used `match` to pick the operation.
This version keeps that logic (see `calculate`) and puts a clickable, keyboard-friendly window on top of it.
Run:  python calculator.py
"""
import tkinter as tk

BG, PANEL, TEXT, MUTED = "#14161c", "#1e212a", "#f3f4f6", "#9ca3af"
NUM, OP, EQ, CLR = "#2a2e39", "#3b4252", "#4f7cff", "#e5484d"


def calculate(a: float, b: float, op: str) -> float:
    """Same operations as the CLI version, with an explicit divide-by-zero error."""
    match op:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return a / b
        case _:
            raise ValueError(f"Unknown operation: {op}")


def fmt(x: float) -> str:
    """Show 7 instead of 7.0, and round long decimals."""
    return str(int(x)) if float(x).is_integer() else f"{x:.10g}"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg=BG, padx=14, pady=14)
        self.resizable(False, False)
        self.first, self.op, self.fresh = None, None, True

        self.history = tk.StringVar(value="")
        self.display = tk.StringVar(value="0")
        tk.Label(self, textvariable=self.history, bg=BG, fg=MUTED, anchor="e",
                 font=("Helvetica", 13)).grid(row=0, column=0, columnspan=4, sticky="ew")
        tk.Label(self, textvariable=self.display, bg=BG, fg=TEXT, anchor="e",
                 font=("Helvetica", 34, "bold")).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))

        layout = [
            ("C", CLR, self.clear), ("±", OP, self.negate), ("%", OP, self.percent), ("/", OP, lambda: self.set_op("/")),
            ("7", NUM, None), ("8", NUM, None), ("9", NUM, None), ("*", OP, lambda: self.set_op("*")),
            ("4", NUM, None), ("5", NUM, None), ("6", NUM, None), ("-", OP, lambda: self.set_op("-")),
            ("1", NUM, None), ("2", NUM, None), ("3", NUM, None), ("+", OP, lambda: self.set_op("+")),
            ("0", NUM, None), (".", NUM, None), ("⌫", OP, self.backspace), ("=", EQ, self.equals),
        ]
        for i, (label, color, cmd) in enumerate(layout):
            action = cmd or (lambda d=label: self.digit(d))
            self.button(label, color, action).grid(row=2 + i // 4, column=i % 4, padx=4, pady=4, sticky="nsew")

        # keyboard support
        for d in "0123456789.":
            self.bind(d, lambda e, d=d: self.digit(d))
        for o in "+-*/":
            self.bind(o, lambda e, o=o: self.set_op(o))
        self.bind("<Return>", lambda e: self.equals())
        self.bind("=", lambda e: self.equals())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())

    def button(self, label, color, action):
        """A Label styled as a button: tk.Button ignores background colours on macOS."""
        b = tk.Label(self, text=label, bg=color, fg=TEXT, width=4, height=2, font=("Helvetica", 18), cursor="hand2")
        hover = "#5b8cff" if color == EQ else "#4a5263"
        b.bind("<Enter>", lambda e: b.configure(bg=hover))
        b.bind("<Leave>", lambda e: b.configure(bg=color))
        b.bind("<Button-1>", lambda e: action())
        return b

    # --- input -------------------------------------------------------------------------------------------
    def digit(self, d: str):
        cur = self.display.get()
        if self.fresh or cur in ("0", "Error"):
            cur = "0." if d == "." else d
            self.fresh = False
        elif d == "." and "." in cur:
            return
        else:
            cur += d
        self.display.set(cur)

    def set_op(self, op: str):
        if self.op and not self.fresh:  # chain: 2 + 3 + … computes 2 + 3 first
            self.equals(keep_history=True)
        try:
            self.first = float(self.display.get())
        except ValueError:
            return
        self.op, self.fresh = op, True
        self.history.set(f"{fmt(self.first)} {op}")

    def equals(self, keep_history: bool = False):
        if self.op is None or self.first is None:
            return
        second = float(self.display.get())
        try:
            result = calculate(self.first, second, self.op)
            if not keep_history:
                self.history.set(f"{fmt(self.first)} {self.op} {fmt(second)} =")
            self.display.set(fmt(result))
        except (ZeroDivisionError, ValueError) as e:
            self.history.set(str(e))
            self.display.set("Error")
        self.first, self.op, self.fresh = None, None, True

    # --- edits -------------------------------------------------------------------------------------------
    def clear(self):
        self.first, self.op, self.fresh = None, None, True
        self.display.set("0")
        self.history.set("")

    def backspace(self):
        if self.fresh:
            return
        cur = self.display.get()[:-1]
        self.display.set(cur if cur not in ("", "-") else "0")

    def negate(self):
        cur = self.display.get()
        if cur not in ("0", "Error"):
            self.display.set(cur[1:] if cur.startswith("-") else "-" + cur)

    def percent(self):
        try:
            self.display.set(fmt(float(self.display.get()) / 100))
        except ValueError:
            pass


if __name__ == "__main__":
    Calculator().mainloop()
