# Getting Started

## Prerequisites
- Python 3.8+
- PIP (Python package manager)
- Virtual Environment (highly recommended)

## Installation

The project relies on the `requests` library.

```Bash
# Clone the repository
git clone https://github.com/Mastau/WPBurst.git
cd wpburst

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Repository Structure

- `cli/`: CLI entry files (e.g., `main.py`).
- `core/`: Main logic (e.g., `enumeration.py`, `module_loader.py`).
- `modules/`: Location for CVE modules. Each module is a separate Python file.
- `lab/`: Configuration files for the testing environment (e.g., `docker-compose.yml`).
- `requirements.txt`: Python dependencies.

## How to Run the Project

```Bash
# Example to scan a target and enumerate plugins
python3 -m cli/main.py -u https://www.example.org
```