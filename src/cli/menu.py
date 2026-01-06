"""CLI menu interface with colors and animations."""

import sys
import re
import time
from datetime import datetime, timedelta
from colorama import init, Fore, Style

from src.models.todo import Todo
from src.services.todo_service import TodoService, CATEGORIES, RECURRENCE_PATTERNS
from src.utils.animations import (
    Spinner,
    typing_effect,
    fade_in_text,
    success_animation,
    error_animation,
    wave_text,
    celebration,
    slide_in_text,
    flash_text,
)

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize colorama for Windows support
init(autoreset=True)

# Color scheme
CYAN = Fore.CYAN
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
WHITE = Fore.WHITE
BLUE = Fore.BLUE
BRIGHT = Style.BRIGHT
DIM = Style.DIM
RESET = Style.RESET_ALL

# Priority colors
PRIORITY_COLORS = {"high": RED, "medium": YELLOW, "low": GREEN}

# Category colors
CATEGORY_COLORS = {
    "work": BLUE,
    "personal": MAGENTA,
    "shopping": GREEN,
    "health": RED,
    "general": CYAN,
}

# Recurrence colors
RECURRENCE_COLORS = {
    "none": DIM,
    "daily": GREEN,
    "weekly": BLUE,
    "monthly": MAGENTA,
}

# Time validation pattern (HH:MM, 24-hour format)
TIME_PATTERN = re.compile(r'^([01]?\d|2[0-3]):[0-5]\d$')


def is_valid_time(time_str: str) -> bool:
    """Validate time format (HH:MM, 24-hour)."""
    if not time_str:
        return False
    return bool(TIME_PATTERN.match(time_str))


def display_reminders(service: TodoService) -> None:
    """Display reminders for overdue and due-now tasks."""
    overdue_todos = service.get_overdue_todos()
    due_now_todos = service.get_due_now_todos()

    if not overdue_todos and not due_now_todos:
        return

    print(f"\n{RED}{BRIGHT}+====================================================+{RESET}")
    print(f"{RED}{BRIGHT}|                    REMINDERS                       |{RESET}")
    print(f"{RED}{BRIGHT}+====================================================+{RESET}")

    if overdue_todos:
        print(f"\n{RED}{BRIGHT}  OVERDUE TASKS ({len(overdue_todos)}):{RESET}")
        today = datetime.now()
        for todo in overdue_todos:
            try:
                due = datetime.strptime(todo.due_date, "%Y-%m-%d")
                days_overdue = (today - due).days
                overdue_text = f"{days_overdue} day{'s' if days_overdue != 1 else ''} overdue"
            except ValueError:
                overdue_text = "overdue"

            time_text = f" @ {todo.due_time}" if todo.due_time else ""
            print(f"  {RED}!{RESET} [{todo.id}] {todo.title[:30]}")
            print(f"       {DIM}Due: {todo.due_date}{time_text} ({overdue_text}){RESET}")

    if due_now_todos:
        print(f"\n{YELLOW}{BRIGHT}  DUE TODAY ({len(due_now_todos)}):{RESET}")
        now = datetime.now()
        for todo in due_now_todos:
            time_text = ""
            status_text = "due today"

            if todo.due_time:
                try:
                    due_hour, due_minute = map(int, todo.due_time.split(":"))
                    due_datetime = now.replace(hour=due_hour, minute=due_minute, second=0, microsecond=0)
                    time_diff = (due_datetime - now).total_seconds() / 60

                    if time_diff < 0:
                        status_text = f"{int(abs(time_diff))} min past due"
                    elif time_diff <= 60:
                        status_text = f"in {int(time_diff)} min"
                    time_text = f" @ {todo.due_time}"
                except ValueError:
                    time_text = f" @ {todo.due_time}"

            print(f"  {YELLOW}!{RESET} [{todo.id}] {todo.title[:30]}")
            print(f"       {DIM}Due: {todo.due_date}{time_text} ({status_text}){RESET}")

    print(f"\n{RED}{BRIGHT}+====================================================+{RESET}\n")


def print_banner() -> None:
    """Display animated banner with effects."""
    # Top border animation
    print()
    border = "+============================================================+"
    slide_in_text(f"{CYAN}{BRIGHT}{border}{RESET}", direction="left", delay=0.008)

    # ASCII art lines with typing effect
    art_lines = [
        f"|                                                            |",
        f"|   {YELLOW}████████╗ ██████╗ ██████╗  ██████╗ {CYAN}                       |",
        f"|   {YELLOW}╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗{CYAN}                       |",
        f"|   {YELLOW}   ██║   ██║   ██║██║  ██║██║   ██║{CYAN}                       |",
        f"|   {YELLOW}   ██║   ██║   ██║██║  ██║██║   ██║{CYAN}                       |",
        f"|   {YELLOW}   ██║   ╚██████╔╝██████╔╝╚██████╔╝{CYAN}                       |",
        f"|   {YELLOW}   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ {CYAN}                       |",
        f"|                                                            |",
    ]

    for line in art_lines:
        print(f"{CYAN}{BRIGHT}{line}{RESET}")
        time.sleep(0.05)

    # Welcome message with wave animation
    wave_text("            *** Welcome to My Todo App ***            ", delay=0.03)

    # Bottom section
    print(f"{CYAN}{BRIGHT}|                                                            |{RESET}")
    slide_in_text(f"{CYAN}{BRIGHT}{border}{RESET}", direction="left", delay=0.008)
    print()


def display_menu() -> None:
    """Display the main menu options with colors."""
    print(f"\n{CYAN}{BRIGHT}+---------------------------------------+{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}           {YELLOW}{BRIGHT}MAIN MENU{RESET}                 {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}+---------------------------------------+{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {GREEN}[1]{RESET} + Add Todo                      {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {GREEN}[2]{RESET}   View All Todos                {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {GREEN}[3]{RESET}   Update Todo                   {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {GREEN}[4]{RESET} x Delete Todo                   {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {GREEN}[5]{RESET} * Mark Complete/Incomplete      {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {BLUE}[6]{RESET}   Search Todos                  {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {MAGENTA}[7]{RESET}   Filter Todos                  {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {YELLOW}[8]{RESET}   Sort Todos                    {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}|{RESET}  {RED}[9]{RESET}   Exit                           {CYAN}{BRIGHT}|{RESET}")
    print(f"{CYAN}{BRIGHT}+---------------------------------------+{RESET}")
    print()


def loading_animation(message: str = "Processing", duration: float = 0.5) -> None:
    """Show a loading spinner animation."""
    frames = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[====]", "[ ===]", "[  ==]", "[   =]"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{CYAN}{frames[i % len(frames)]} {message}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()


def typewriter(text: str, delay: float = 0.03) -> None:
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def celebrate() -> None:
    """Show enhanced celebration animation."""
    # Use the new celebration animation
    celebration("Task Complete!")


def pulse_text(text: str, color: str = CYAN, times: int = 2) -> None:
    """Pulse text effect."""
    for _ in range(times):
        sys.stdout.write(f"\r{DIM}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write(f"\r{color}{BRIGHT}{text}{RESET}")
        sys.stdout.flush()
        time.sleep(0.15)
    print()


def success_message(text: str) -> None:
    """Display success message with animation."""
    success_animation(text)


def error_message(text: str) -> None:
    """Display error message with animation."""
    error_animation(text)


def info_message(text: str) -> None:
    print(f"\n{CYAN}[INFO] {text}{RESET}")


def get_priority_display(priority: str) -> str:
    """Get colored priority display."""
    color = PRIORITY_COLORS.get(priority, YELLOW)
    symbols = {"high": "!!!", "medium": "!!", "low": "!"}
    symbol = symbols.get(priority, "!!")
    return f"{color}{symbol} {priority.upper()}{RESET}"


def get_category_display(category: str) -> str:
    """Get colored category display."""
    color = CATEGORY_COLORS.get(category, CYAN)
    icons = {"work": "[W]", "personal": "[P]", "shopping": "[S]", "health": "[H]", "general": "[G]"}
    icon = icons.get(category, "[G]")
    return f"{color}{icon} {category.capitalize()}{RESET}"


def get_due_date_display(due_date: str) -> str:
    """Get colored due date display."""
    if not due_date:
        return ""

    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        diff = (due - today).days

        if diff < 0:
            return f"{RED}OVERDUE ({due_date}){RESET}"
        elif diff == 0:
            return f"{RED}TODAY{RESET}"
        elif diff == 1:
            return f"{YELLOW}Tomorrow{RESET}"
        elif diff <= 7:
            return f"{YELLOW}{diff} days left{RESET}"
        else:
            return f"{GREEN}{due_date}{RESET}"
    except ValueError:
        return f"{DIM}{due_date}{RESET}"


def get_recurrence_display(recurrence: str) -> str:
    """Get colored recurrence display."""
    if recurrence == "none":
        return ""
    color = RECURRENCE_COLORS.get(recurrence, DIM)
    icons = {"daily": "[D]", "weekly": "[W]", "monthly": "[M]"}
    icon = icons.get(recurrence, "")
    return f"{color}{icon} {recurrence.capitalize()}{RESET}"


def format_todo(todo: Todo, index: int = 0) -> str:
    """Format a todo for display with colors."""
    if todo.completed:
        checkbox = f"{GREEN}[X]{RESET}"
        title_color = f"{DIM}{GREEN}"
        status = f"{GREEN}DONE{RESET}"
    else:
        checkbox = f"{YELLOW}[ ]{RESET}"
        title_color = f"{WHITE}{BRIGHT}"
        status = f"{YELLOW}PENDING{RESET}"

    priority_display = get_priority_display(todo.priority)
    category_display = get_category_display(todo.category)
    due_display = get_due_date_display(todo.due_date)
    recurrence_display = get_recurrence_display(todo.recurrence)

    title_display = todo.title[:26]
    result = f"""
{CYAN}+--------------------------------------------------+{RESET}
{CYAN}|{RESET} {MAGENTA}ID: {todo.id:<3}{RESET} {checkbox} {title_color}{title_display:<26}{RESET} {status} {CYAN}|{RESET}
{CYAN}|{RESET}       {priority_display:<20} {category_display:<18} {CYAN}|{RESET}"""

    if due_display:
        # Include time if present
        time_part = f" @ {todo.due_time}" if todo.due_time else ""
        result += f"""
{CYAN}|{RESET}       Due: {due_display}{time_part:<24} {CYAN}|{RESET}"""

    if recurrence_display:
        result += f"""
{CYAN}|{RESET}       Recurs: {recurrence_display:<33} {CYAN}|{RESET}"""

    if todo.description:
        desc = todo.description[:40]
        result += f"""
{CYAN}|{RESET}       {DIM}> {desc:<40}{RESET} {CYAN}|{RESET}"""

    result += f"""
{CYAN}+--------------------------------------------------+{RESET}"""
    return result


def print_section_header(title: str) -> None:
    """Print a styled section header with fade-in animation."""
    print()
    line = "=" * 50

    # Fade in the top line
    fade_in_text(line, delay=0.01)

    # Fade in the title
    fade_in_text(f"  {title}", delay=0.02)

    # Quick bottom line
    print(f"{MAGENTA}{BRIGHT}{line}{RESET}")


def get_priority_input() -> str:
    """Get priority input from user."""
    print(f"\n{CYAN}Priority:{RESET}")
    print(f"  {RED}[1]{RESET} High   (!!!)")
    print(f"  {YELLOW}[2]{RESET} Medium (!!)  - Default")
    print(f"  {GREEN}[3]{RESET} Low    (!)")

    choice = input(f"{CYAN}Select (1-3, Enter for Medium): {RESET}").strip()

    if choice == "1":
        return "high"
    elif choice == "3":
        return "low"
    else:
        return "medium"


def get_category_input() -> str:
    """Get category input from user."""
    print(f"\n{CYAN}Category:{RESET}")
    print(f"  {BLUE}[1]{RESET} Work")
    print(f"  {MAGENTA}[2]{RESET} Personal")
    print(f"  {GREEN}[3]{RESET} Shopping")
    print(f"  {RED}[4]{RESET} Health")
    print(f"  {CYAN}[5]{RESET} General - Default")

    choice = input(f"{CYAN}Select (1-5, Enter for General): {RESET}").strip()

    category_map = {"1": "work", "2": "personal", "3": "shopping", "4": "health", "5": "general"}
    return category_map.get(choice, "general")


def get_due_date_input() -> str:
    """Get due date input from user."""
    print(f"\n{CYAN}Due Date (YYYY-MM-DD format):{RESET}")
    print(f"  {DIM}Examples: 2025-12-31, 2025-01-15{RESET}")
    print(f"  {DIM}Press Enter to skip{RESET}")

    due_date = input(f"{CYAN}Enter date: {RESET}").strip()

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            return due_date
        except ValueError:
            error_message("Invalid date format! Skipping due date.")
            return ""
    return ""


def get_due_time_input() -> str:
    """Get due time input from user."""
    print(f"\n{CYAN}Due Time (HH:MM, 24-hour format):{RESET}")
    print(f"  {DIM}Examples: 09:00, 14:30, 23:59{RESET}")
    print(f"  {DIM}Press Enter to skip{RESET}")

    while True:
        due_time = input(f"{CYAN}Enter time: {RESET}").strip()

        if not due_time:
            return ""

        if is_valid_time(due_time):
            return due_time
        else:
            error_message("Invalid time format! Use HH:MM (e.g., 09:00, 14:30)")


def get_recurrence_input() -> str:
    """Get recurrence pattern input from user."""
    print(f"\n{CYAN}Recurrence Pattern:{RESET}")
    print(f"  {GREEN}[1]{RESET} Daily   - Repeats every day")
    print(f"  {BLUE}[2]{RESET} Weekly  - Repeats every 7 days")
    print(f"  {MAGENTA}[3]{RESET} Monthly - Repeats same day each month")
    print(f"  {DIM}[4]{RESET} None    - One-time task (Default)")

    choice = input(f"{CYAN}Select (1-4, Enter for None): {RESET}").strip()

    recurrence_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "none"}
    return recurrence_map.get(choice, "none")


def display_todos(todos: list[Todo], title: str = "RESULTS") -> None:
    """Display a list of todos."""
    print_section_header(title)

    if not todos:
        info_message("No todos found!")
        return

    completed = sum(1 for t in todos if t.completed)
    total = len(todos)
    progress = completed / total if total > 0 else 0
    bar_length = 30
    filled = int(bar_length * progress)
    bar = f"{GREEN}{'#' * filled}{DIM}{'-' * (bar_length - filled)}{RESET}"

    print(f"\n{CYAN}Progress: [{bar}] {YELLOW}{completed}/{total}{RESET} ({int(progress * 100)}%)")

    for i, todo in enumerate(todos):
        print(format_todo(todo, i))


def handle_add_todo(service: TodoService) -> None:
    """Handle adding a new todo."""
    print_section_header("+ ADD NEW TODO")

    title = input(f"{CYAN}Enter title: {RESET}")
    if not title.strip():
        error_message("Title cannot be empty!")
        return

    description = input(f"{CYAN}Enter description (optional): {RESET}")
    priority = get_priority_input()
    category = get_category_input()
    due_date = get_due_date_input()

    # Only prompt for time if date is set
    due_time = ""
    if due_date:
        due_time = get_due_time_input()

    recurrence = get_recurrence_input()

    loading_animation("Creating todo")

    todo = service.add(title, description, priority, due_date, category, due_time, recurrence)
    if todo:
        pulse_text(f"  + Todo #{todo.id} Created!", GREEN, 2)
        success_message(f"Todo added successfully! (ID: {YELLOW}{todo.id}{GREEN})")
        if todo.recurrence != "none":
            info_message(f"This task will recur {todo.recurrence}.")
    else:
        error_message("Failed to add todo!")


def handle_view_todos(service: TodoService) -> None:
    """Handle viewing all todos."""
    todos = service.get_all()
    loading_animation("Fetching todos")
    display_todos(todos, "YOUR TODOS")

    if not todos:
        print(f"\n{DIM}  Tip: Press {GREEN}1{RESET}{DIM} to add your first todo!{RESET}")


def handle_update_todo(service: TodoService) -> None:
    """Handle updating an existing todo."""
    print_section_header("UPDATE TODO")

    id_input = input(f"{CYAN}Enter Todo ID to update: {RESET}").strip()

    try:
        todo_id = int(id_input)
    except ValueError:
        error_message("Please enter a valid number!")
        return

    todo = service.get_by_id(todo_id)
    if not todo:
        error_message(f"Todo with ID {todo_id} not found!")
        return

    print(f"\n{YELLOW}Current Todo:{RESET}")
    print(format_todo(todo))

    print(f"\n{DIM}(Press Enter to keep current value){RESET}")

    new_title = input(f"{CYAN}New title: {RESET}").strip()
    new_description = input(f"{CYAN}New description: {RESET}")

    # Priority update
    print(f"\n{CYAN}New priority? (h=high, m=medium, l=low, Enter=keep): {RESET}", end="")
    priority_input = input().strip().lower()
    new_priority = None
    if priority_input == "h":
        new_priority = "high"
    elif priority_input == "m":
        new_priority = "medium"
    elif priority_input == "l":
        new_priority = "low"

    # Category update
    print(f"{CYAN}New category? (w=work, p=personal, s=shopping, h=health, g=general, Enter=keep): {RESET}", end="")
    cat_input = input().strip().lower()
    new_category = None
    cat_map = {"w": "work", "p": "personal", "s": "shopping", "h": "health", "g": "general"}
    if cat_input in cat_map:
        new_category = cat_map[cat_input]

    # Due date update
    new_due_date = input(f"{CYAN}New due date (YYYY-MM-DD, Enter=keep): {RESET}").strip()
    if new_due_date:
        try:
            datetime.strptime(new_due_date, "%Y-%m-%d")
        except ValueError:
            error_message("Invalid date format! Keeping current date.")
            new_due_date = None

    # Due time update (only if todo has or will have a date)
    new_due_time = None
    has_date = new_due_date or todo.due_date
    if has_date:
        print(f"{CYAN}New due time? (HH:MM 24-hour, c=clear, Enter=keep): {RESET}", end="")
        time_input = input().strip()
        if time_input.lower() == "c":
            new_due_time = ""  # Clear the time
        elif time_input:
            if is_valid_time(time_input):
                new_due_time = time_input
            else:
                error_message("Invalid time format! Keeping current time.")

    # Recurrence update (d=daily, w=weekly, m=monthly, n=none, Enter=keep)
    print(f"{CYAN}New recurrence? (d=daily, w=weekly, m=monthly, n=none, Enter=keep): {RESET}", end="")
    rec_input = input().strip().lower()
    new_recurrence = None
    rec_map = {"d": "daily", "w": "weekly", "m": "monthly", "n": "none"}
    if rec_input in rec_map:
        new_recurrence = rec_map[rec_input]

    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None
    due_date_to_update = new_due_date if new_due_date else None

    if all(v is None for v in [title_to_update, description_to_update, new_priority, new_category, due_date_to_update, new_due_time, new_recurrence]):
        info_message("No changes made.")
        return

    loading_animation("Updating todo")

    result = service.update(
        todo_id,
        title_to_update,
        description_to_update,
        new_priority,
        due_date_to_update,
        new_category,
        new_due_time,
        new_recurrence
    )
    if result:
        success_message("Todo updated successfully!")
    else:
        error_message("Title cannot be empty!")


def handle_delete_todo(service: TodoService) -> None:
    """Handle deleting a todo."""
    print_section_header("DELETE TODO")

    id_input = input(f"{CYAN}Enter Todo ID to delete: {RESET}").strip()

    try:
        todo_id = int(id_input)
    except ValueError:
        error_message("Please enter a valid number!")
        return

    todo = service.get_by_id(todo_id)
    if not todo:
        error_message(f"Todo with ID {todo_id} not found!")
        return

    print(f"\n{YELLOW}About to delete:{RESET}")
    print(format_todo(todo))

    confirm = input(f"\n{RED}Are you sure? (y/N): {RESET}").strip().lower()

    if confirm == 'y':
        loading_animation("Deleting todo")
        if service.delete(todo_id):
            success_message("Todo deleted successfully!")
    else:
        info_message("Deletion cancelled.")


def handle_mark_todo(service: TodoService) -> None:
    """Handle marking a todo as complete or incomplete."""
    print_section_header("MARK TODO")

    id_input = input(f"{CYAN}Enter Todo ID: {RESET}").strip()

    try:
        todo_id = int(id_input)
    except ValueError:
        error_message("Please enter a valid number!")
        return

    todo = service.get_by_id(todo_id)
    if not todo:
        error_message(f"Todo with ID {todo_id} not found!")
        return

    print(f"\n{YELLOW}Current Todo:{RESET}")
    print(format_todo(todo))

    if todo.completed:
        status_text = f"{GREEN}Complete [X]{RESET}"
    else:
        status_text = f"{YELLOW}Incomplete [ ]{RESET}"

    print(f"\n{CYAN}Current status: {status_text}")

    choice = input(f"\n{CYAN}Mark as {GREEN}(c)omplete{RESET} or {YELLOW}(i)ncomplete{RESET}? ").strip().lower()

    if choice in ("c", "complete"):
        loading_animation("Marking complete")
        completed_todo, new_todo = service.set_completed(todo_id, True)
        if completed_todo:
            celebrate()
            success_message("Todo marked as complete!")
            # Display next occurrence message for recurring tasks
            if new_todo:
                print(f"\n{MAGENTA}{BRIGHT}Recurring Task:{RESET}")
                print(f"  {GREEN}Next occurrence created:{RESET} Todo #{new_todo.id}")
                print(f"  {CYAN}Due Date:{RESET} {new_todo.due_date or 'Not set'}")
                if new_todo.due_time:
                    print(f"  {CYAN}Due Time:{RESET} {new_todo.due_time}")
                print(f"  {CYAN}Recurrence:{RESET} {new_todo.recurrence.capitalize()}")
    elif choice in ("i", "incomplete"):
        loading_animation("Marking incomplete")
        completed_todo, _ = service.set_completed(todo_id, False)
        if completed_todo:
            success_message("Todo marked as incomplete!")
    else:
        error_message("Please enter 'c' for complete or 'i' for incomplete.")


def handle_search(service: TodoService) -> None:
    """Handle searching todos."""
    print_section_header("SEARCH TODOS")

    query = input(f"{CYAN}Enter search term: {RESET}").strip()

    if not query:
        error_message("Please enter a search term!")
        return

    loading_animation("Searching")
    results = service.search(query)

    display_todos(results, f"SEARCH RESULTS: '{query}'")


def handle_filter(service: TodoService) -> None:
    """Handle filtering todos."""
    print_section_header("FILTER TODOS")

    print(f"\n{CYAN}Filter by:{RESET}")
    print(f"  {GREEN}[1]{RESET} Status (Pending/Complete)")
    print(f"  {BLUE}[2]{RESET} Category")
    print(f"  {YELLOW}[3]{RESET} Priority")
    print(f"  {RED}[4]{RESET} Due Date Status")

    choice = input(f"{CYAN}Select filter type (1-4): {RESET}").strip()

    if choice == "1":
        print(f"\n{CYAN}Status:{RESET}")
        print(f"  {YELLOW}[1]{RESET} Pending only")
        print(f"  {GREEN}[2]{RESET} Completed only")
        print(f"  {CYAN}[3]{RESET} All")

        status_choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        loading_animation("Filtering")

        if status_choice == "1":
            todos = service.filter_by_status(completed=False)
            display_todos(todos, "PENDING TODOS")
        elif status_choice == "2":
            todos = service.filter_by_status(completed=True)
            display_todos(todos, "COMPLETED TODOS")
        else:
            todos = service.get_all()
            display_todos(todos, "ALL TODOS")

    elif choice == "2":
        print(f"\n{CYAN}Category:{RESET}")
        for i, cat in enumerate(CATEGORIES, 1):
            color = CATEGORY_COLORS.get(cat, CYAN)
            print(f"  {color}[{i}]{RESET} {cat.capitalize()}")

        cat_choice = input(f"{CYAN}Select (1-{len(CATEGORIES)}): {RESET}").strip()

        try:
            cat_index = int(cat_choice) - 1
            if 0 <= cat_index < len(CATEGORIES):
                category = CATEGORIES[cat_index]
                loading_animation("Filtering")
                todos = service.filter_by_category(category)
                display_todos(todos, f"{category.upper()} TODOS")
            else:
                error_message("Invalid selection!")
        except ValueError:
            error_message("Please enter a number!")

    elif choice == "3":
        print(f"\n{CYAN}Priority:{RESET}")
        print(f"  {RED}[1]{RESET} High")
        print(f"  {YELLOW}[2]{RESET} Medium")
        print(f"  {GREEN}[3]{RESET} Low")

        pri_choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        pri_map = {"1": "high", "2": "medium", "3": "low"}

        if pri_choice in pri_map:
            priority = pri_map[pri_choice]
            loading_animation("Filtering")
            todos = service.filter_by_priority(priority)
            display_todos(todos, f"{priority.upper()} PRIORITY TODOS")
        else:
            error_message("Invalid selection!")

    elif choice == "4":
        print(f"\n{CYAN}Due Date Status:{RESET}")
        print(f"  {RED}[1]{RESET} Overdue")
        print(f"  {YELLOW}[2]{RESET} Due Today")
        print(f"  {GREEN}[3]{RESET} Upcoming (next 7 days)")

        due_choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        loading_animation("Filtering")

        if due_choice == "1":
            todos = service.filter_by_due_status("overdue")
            display_todos(todos, "OVERDUE TODOS")
        elif due_choice == "2":
            todos = service.filter_by_due_status("today")
            display_todos(todos, "DUE TODAY")
        elif due_choice == "3":
            todos = service.filter_by_due_status("upcoming")
            display_todos(todos, "UPCOMING (Next 7 Days)")
        else:
            error_message("Invalid selection!")
    else:
        error_message("Invalid filter type!")


def handle_sort(service: TodoService) -> None:
    """Handle sorting todos."""
    print_section_header("SORT TODOS")

    print(f"\n{CYAN}Sort by:{RESET}")
    print(f"  {YELLOW}[1]{RESET} Priority (High -> Low)")
    print(f"  {BLUE}[2]{RESET} Due Date (Earliest first)")
    print(f"  {CYAN}[3]{RESET} ID (Default)")

    choice = input(f"{CYAN}Select sort order (1-3): {RESET}").strip()

    loading_animation("Sorting")

    if choice == "1":
        todos = service.sort_by_priority()
        display_todos(todos, "SORTED BY PRIORITY")
    elif choice == "2":
        todos = service.sort_by_due_date()
        display_todos(todos, "SORTED BY DUE DATE")
    else:
        todos = service.get_all()
        display_todos(todos, "SORTED BY ID")


def handle_stats(service: TodoService) -> None:
    """Handle displaying statistics."""
    print_section_header("STATISTICS")

    loading_animation("Calculating")
    stats = service.get_stats()

    total = stats["total"]
    completed = stats["completed"]
    pending = stats["pending"]
    progress = (completed / total * 100) if total > 0 else 0

    print(f"\n{CYAN}{BRIGHT}Overview:{RESET}")
    print(f"  Total Todos:     {YELLOW}{total}{RESET}")
    print(f"  Completed:       {GREEN}{completed}{RESET}")
    print(f"  Pending:         {YELLOW}{pending}{RESET}")

    # Progress bar
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = f"{GREEN}{'#' * filled}{DIM}{'-' * (bar_length - filled)}{RESET}"
    print(f"  Progress:        [{bar}] {int(progress)}%")

    if stats["overdue"] > 0:
        print(f"  {RED}Overdue:         {stats['overdue']}{RESET}")

    print(f"\n{CYAN}{BRIGHT}By Priority (Pending):{RESET}")
    print(f"  {RED}High:   {stats['by_priority']['high']}{RESET}")
    print(f"  {YELLOW}Medium: {stats['by_priority']['medium']}{RESET}")
    print(f"  {GREEN}Low:    {stats['by_priority']['low']}{RESET}")

    print(f"\n{CYAN}{BRIGHT}By Category (All):{RESET}")
    for cat, count in stats["by_category"].items():
        color = CATEGORY_COLORS.get(cat, CYAN)
        print(f"  {color}{cat.capitalize()}: {count}{RESET}")


def goodbye_animation() -> None:
    """Display enhanced goodbye animation."""
    # Saving spinner
    spinner = Spinner("Saving your data", style="dots", color="cyan")
    spinner.start()
    time.sleep(0.8)
    spinner.stop("Data saved!", success=True)

    print()

    # Goodbye with wave effect
    wave_text("  Goodbye! See you soon!  ", delay=0.05)

    # Final flash
    flash_text("  Thank you for using Todo App!  ", times=2, delay=0.12, color="yellow")
    print()


def startup_animation() -> None:
    """Show startup loading animation with spinner."""
    # Phase 1: Spinner loading
    spinner = Spinner("Initializing Todo App", style="dots", color="cyan")
    spinner.start()
    time.sleep(1.2)
    spinner.stop("System ready!", success=True)

    # Phase 2: Progress bar
    stages = ["Loading modules", "Checking data", "Ready"]
    for i, stage in enumerate(stages):
        frames = [
            f"{CYAN}[          ]{RESET}",
            f"{CYAN}[===       ]{RESET}",
            f"{CYAN}[======    ]{RESET}",
            f"{GREEN}[==========]{RESET}",
        ]
        for frame in frames:
            sys.stdout.write(f"\r  {frame} {stage}...")
            sys.stdout.flush()
            time.sleep(0.08)

    sys.stdout.write(f"\r  {GREEN}[==========]{RESET} All systems go!    \n")
    time.sleep(0.3)


def run_cli() -> None:
    """Run the main CLI loop."""
    service = TodoService()

    try:
        startup_animation()
        print_banner()

        while True:
            display_reminders(service)
            display_menu()
            choice = input(f"{YELLOW}{BRIGHT}>> Enter choice (1-9): {RESET}").strip()

            if choice == "1":
                handle_add_todo(service)
            elif choice == "2":
                handle_view_todos(service)
            elif choice == "3":
                handle_update_todo(service)
            elif choice == "4":
                handle_delete_todo(service)
            elif choice == "5":
                handle_mark_todo(service)
            elif choice == "6":
                handle_search(service)
            elif choice == "7":
                handle_filter(service)
            elif choice == "8":
                handle_sort(service)
            elif choice == "9":
                goodbye_animation()
                break
            else:
                error_message("Please enter a number between 1 and 9.")
    except KeyboardInterrupt:
        print(f"\n\n{CYAN}Goodbye! Data saved.{RESET}")
    except EOFError:
        print(f"\n\n{CYAN}Goodbye! Data saved.{RESET}")
