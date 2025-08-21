# mux-tools

A tmux session and window management utility built with Python 3.10+ features and libtmux.

## 🐍 Python Version

This project is configured for **Python 3.10** and above. The `pyproject.toml` specifies `requires-python = ">=3.10"`.

## 🚀 Quick Start

### Prerequisites

1. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip
   pip install uv
   ```

2. **Verify uv installation**:
   ```bash
   uv --version
   ```

### Project Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tianhuil/mux-tools.git
   cd mux-tools
   ```

2. **Create a virtual environment with Python 3.10**:
   ```bash
   uv venv --python 3.10
   ```

3. **Activate the virtual environment**:
   ```bash
   # On macOS/Linux
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv pip install -e .
   ```

5. **Install development dependencies**:
   ```bash
   uv pip install -e ".[dev]"
   ```

## 📁 Project Structure

```
mux-tools/
├── src/
│   └── mux/
│       ├── __init__.py
│       ├── cli.py         # Tmux CLI interface (argparse + libtmux)
│       └── demo.py        # Demo functionality
├── tests/
│   ├── __init__.py
│   └── test_demo.py
├── docs/
├── pyproject.toml         # Project configuration and dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── CHANGELOG.md          # Version history
├── .gitignore           # Git ignore patterns
└── .venv/               # Virtual environment (created by uv)
```

## 🚀 Installation

### From PyPI (when published)
```bash
pip install mux-tools
```

### From source
```bash
git clone https://github.com/tianhuil/mux-tools.git
cd mux-tools
uv pip install -e .
```

## 🖥️ Command Line Usage

After installation, you can use the following tmux management commands:

```bash
# Main CLI tool
mux --help

# Session management
mux session new myproject     # Create and attach to new session
mux session attach myproject  # Attach to existing session
mux session list             # List all sessions

# Window management
mux window new               # Create new window
mux window goto 3            # Go to window 3
mux window close             # Close current window
mux window list              # List windows in current session
```

## 🛠️ Development Workflow

### Adding Dependencies

```bash
# Add a production dependency
uv add requests

# Add a development dependency
uv add --dev pytest

# Add with specific version
uv add "pandas>=2.0.0"

# Add from a group
uv add --group dev black
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_main.py

# Run with specific markers
uv run pytest -m "not slow"
```

### Code Quality

```bash
# Format code with black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Type checking with mypy
uv run mypy src/

# Linting with flake8
uv run flake8 src/ tests/
```

### Building and Publishing

```bash
# Build the package
uv run python -m build

# Install in development mode
uv pip install -e .

# Install in production mode
uv pip install .
```

## 🔧 Configuration

### Python Version Management

The project is configured for Python 3.10+ in `pyproject.toml`:

```toml
[project]
requires-python = ">=3.10"
```

### Tool Configurations

- **Black**: Code formatting with 88 character line length
- **isort**: Import sorting compatible with Black
- **mypy**: Type checking with strict settings for Python 3.10
- **pytest**: Testing framework with coverage support
- **coverage**: Code coverage reporting

### Dependency Groups

- **main**: Production dependencies
- **dev**: Development tools (testing, formatting, linting)
- **test**: Testing-specific dependencies
- **docs**: Documentation generation tools

## 🐛 Troubleshooting

### Python Version Issues

If you encounter Python version issues:

1. **Check available Python versions**:
   ```bash
   uv python list
   ```

2. **Install Python 3.10 if needed**:
   ```bash
   uv python install 3.10
   ```

3. **Create environment with specific version**:
   ```bash
   uv venv --python 3.10
   ```

### Virtual Environment Issues

If the virtual environment isn't working:

1. **Remove and recreate**:
   ```bash
   rm -rf .venv
   uv venv --python 3.10
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install -e .
   ```

2. **Check uv cache**:
   ```bash
   uv cache clean
   ```

### Dependency Resolution Issues

If you encounter dependency conflicts:

1. **Update uv**:
   ```bash
   uv self update
   ```

2. **Clean and reinstall**:
   ```bash
   uv pip uninstall --all
   uv pip install -e .
   ```

## 📚 Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python 3.10 Documentation](https://docs.python.org/3.10/)
- [pyproject.toml Specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [Hatchling Build Backend](https://hatch.pypa.io/latest/build/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks:
   ```bash
   uv run pytest
   uv run black src/ tests/
   uv run isort src/ tests/
   uv run mypy src/
   uv run flake8 src/ tests/
   ```
5. Commit your changes
6. Push to your branch
7. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
