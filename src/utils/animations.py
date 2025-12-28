"""Terminal animations and visual effects for CLI."""

import sys
import time
import threading
from colorama import Fore, Style, init

# Initialize colorama and fix Windows encoding
init(autoreset=True)
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7


class Spinner:
    """Animated loading spinner."""

    # ASCII-compatible spinner frames for Windows
    FRAMES = ["|", "/", "-", "\\"]
    DOTS = [".", "..", "...", "...."]
    ARROWS = ["<-", "^", "->", "v"]
    BOUNCE = ["o", "O", "o", "."]
    BAR = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[====]", "[ ===]", "[  ==]", "[   =]"]

    def __init__(self, message: str = "Loading", style: str = "dots", color: str = "cyan"):
        self.message = message
        self.frames = getattr(self, style.upper(), self.DOTS)
        self.color = getattr(Fore, color.upper(), Fore.CYAN)
        self._running = False
        self._thread = None
        self._frame_idx = 0

    def _animate(self):
        while self._running:
            frame = self.frames[self._frame_idx % len(self.frames)]
            sys.stdout.write(f"\r{self.color}{frame}{Style.RESET_ALL} {self.message}")
            sys.stdout.flush()
            self._frame_idx += 1
            time.sleep(0.1)

    def start(self):
        """Start the spinner animation."""
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self, final_message: str = "", success: bool = True):
        """Stop the spinner with optional final message."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.2)

        # Clear the line
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")

        if final_message:
            icon = f"{Fore.GREEN}✓{Style.RESET_ALL}" if success else f"{Fore.RED}✗{Style.RESET_ALL}"
            print(f"{icon} {final_message}")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def typing_effect(text: str, delay: float = 0.03, color: str = None):
    """Print text with typewriter effect."""
    if color:
        color_code = getattr(Fore, color.upper(), "")
        sys.stdout.write(color_code)

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    if color:
        sys.stdout.write(Style.RESET_ALL)
    print()


def fade_in_text(text: str, delay: float = 0.05):
    """Simulate fade-in by revealing text progressively."""
    for i in range(len(text) + 1):
        sys.stdout.write(f"\r{Fore.CYAN}{text[:i]}{Fore.LIGHTBLACK_EX}{text[i:]}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def success_animation(message: str = "Success!"):
    """Display success animation with checkmark."""
    frames = [
        f"{Fore.GREEN}[    ]{Style.RESET_ALL}",
        f"{Fore.GREEN}[=   ]{Style.RESET_ALL}",
        f"{Fore.GREEN}[==  ]{Style.RESET_ALL}",
        f"{Fore.GREEN}[=== ]{Style.RESET_ALL}",
        f"{Fore.GREEN}[====]{Style.RESET_ALL}",
        f"{Fore.GREEN}[ OK ]{Style.RESET_ALL}",
    ]

    for frame in frames:
        sys.stdout.write(f"\r{frame} {message}")
        sys.stdout.flush()
        time.sleep(0.08)
    print()


def error_animation(message: str = "Error!"):
    """Display error animation with X mark."""
    frames = [
        f"{Fore.RED}[    ]{Style.RESET_ALL}",
        f"{Fore.RED}[=   ]{Style.RESET_ALL}",
        f"{Fore.RED}[==  ]{Style.RESET_ALL}",
        f"{Fore.RED}[=== ]{Style.RESET_ALL}",
        f"{Fore.RED}[====]{Style.RESET_ALL}",
        f"{Fore.RED}[ X  ]{Style.RESET_ALL}",
    ]

    for frame in frames:
        sys.stdout.write(f"\r{frame} {message}")
        sys.stdout.flush()
        time.sleep(0.08)
    print()


def progress_bar(current: int, total: int, width: int = 30, label: str = ""):
    """Display an animated progress bar."""
    if total == 0:
        percent = 100
    else:
        percent = int((current / total) * 100)

    filled = int(width * current / total) if total > 0 else width
    bar = "#" * filled + "-" * (width - filled)

    color = Fore.GREEN if percent == 100 else Fore.CYAN
    sys.stdout.write(f"\r{label}{color}[{bar}]{Style.RESET_ALL} {percent}%")
    sys.stdout.flush()

    if current >= total:
        print()


def slide_in_text(text: str, direction: str = "left", delay: float = 0.02):
    """Slide text in from left or right."""
    width = len(text)

    if direction == "left":
        for i in range(width + 1):
            spaces = " " * (width - i)
            sys.stdout.write(f"\r{spaces}{text[:i]}")
            sys.stdout.flush()
            time.sleep(delay)
    else:  # right
        for i in range(width + 1):
            sys.stdout.write(f"\r{text[-i:] if i > 0 else ''}{' ' * (width - i)}")
            sys.stdout.flush()
            time.sleep(delay)
    print()


def flash_text(text: str, times: int = 3, delay: float = 0.15, color: str = "yellow"):
    """Flash text on and off."""
    color_code = getattr(Fore, color.upper(), Fore.YELLOW)

    for _ in range(times):
        sys.stdout.write(f"\r{color_code}{text}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write(f"\r{' ' * len(text)}")
        sys.stdout.flush()
        time.sleep(delay / 2)

    sys.stdout.write(f"\r{color_code}{text}{Style.RESET_ALL}")
    print()


def wave_text(text: str, delay: float = 0.1):
    """Display text with wave animation (colors ripple through)."""
    colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA]

    for offset in range(len(text) + len(colors)):
        output = ""
        for i, char in enumerate(text):
            color_idx = (offset - i) % len(colors)
            if 0 <= offset - i < len(colors):
                output += colors[color_idx] + char
            else:
                output += Fore.WHITE + char
        sys.stdout.write(f"\r{output}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def celebration(message: str = "Complete!"):
    """Display a celebration animation."""
    frames = [
        "  *  ",
        " *** ",
        "*****",
        " *** ",
        "  *  ",
    ]

    colors = [Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.RED]
    for i in range(10):
        color = colors[i % len(colors)]
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{color}{frame}{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL} {color}{frame}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.12)
    print()


def banner_reveal(lines: list[str], delay: float = 0.05):
    """Reveal a multi-line banner with animation."""
    for line in lines:
        typing_effect(line, delay=delay, color="CYAN")
        time.sleep(0.1)
