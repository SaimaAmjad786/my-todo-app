# Quickstart: Todo CLI Core (Phase I)

**Feature**: 001-todo-cli-core
**Date**: 2025-12-26

## Prerequisites

- Python 3.13 or higher
- UV package manager (https://docs.astral.sh/uv/)

## Installation

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd todo-app

# Install UV if not already installed
# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize the project (creates virtual environment)
uv sync
```

## Running the Application

```bash
# Run the Todo CLI
uv run python -m src.main

# Or using the script entry point (after setup)
uv run todo
```

## Usage

When you start the application, you'll see an interactive menu:

```
=== Todo Application ===
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

### Adding a Todo

```
Enter choice (1-6): 1

Enter title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

Todo added successfully! (ID: 1)
```

### Viewing All Todos

```
Enter choice (1-6): 2

=== Your Todos ===
ID: 1 [ ] Buy groceries
      Description: Milk, eggs, bread

ID: 2 [x] Call mom
```

### Updating a Todo

```
Enter choice (1-6): 3

Enter Todo ID to update: 1
Enter new title (press Enter to keep current): Buy organic groceries
Enter new description (press Enter to keep current):

Todo updated successfully!
```

### Deleting a Todo

```
Enter choice (1-6): 4

Enter Todo ID to delete: 2

Todo deleted successfully!
```

### Marking Complete/Incomplete

```
Enter choice (1-6): 5

Enter Todo ID: 1
Mark as (c)omplete or (i)ncomplete? c

Todo marked as complete!
```

### Exiting

```
Enter choice (1-6): 6

Goodbye!
```

## Error Handling

The application handles errors gracefully:

```
# Invalid menu choice
Enter choice (1-6): 7
Error: Please enter a number between 1 and 6.

# Empty title
Enter title:
Error: Title cannot be empty.

# Non-existent ID
Enter Todo ID to update: 99
Error: Todo with ID 99 not found.

# Invalid ID format
Enter Todo ID: abc
Error: Please enter a valid number.
```

## Project Structure

```
todo-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py          # Todo dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py  # Business logic
│   └── cli/
│       ├── __init__.py
│       └── menu.py          # User interface
├── specs/
│   └── 001-todo-cli-core/   # Feature documentation
├── pyproject.toml
└── README.md
```

## Limitations (Phase I)

- **No persistence**: Todos are lost when the application exits
- **Single user**: No authentication or user accounts
- **No advanced features**: No tags, priorities, or due dates
- **No search**: Cannot filter or search todos

These limitations are intentional for Phase I and will be addressed in future phases.

## Troubleshooting

### "Python not found"

Ensure Python 3.13+ is installed and in your PATH:
```bash
python --version
# Should show Python 3.13.x or higher
```

### "UV not found"

Reinstall UV following the installation instructions above.

### "Module not found"

Ensure you're running from the project root directory:
```bash
cd todo-app
uv run python -m src.main
```
