#!/bin/zsh

# Start the Poverty Resource Allocation Streamlit application.

echo "Starting the Poverty Resource Allocation System..."

# Resolve the absolute path to this script's directory.
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" &> /dev/null && pwd)

# Resolve Python interpreter: prefer project venv, fallback to system python3.
PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON_EXEC" ]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_EXEC=$(command -v python3)
        echo "Warning: project virtual environment not found, using system Python: $PYTHON_EXEC"
    else
        echo "Error: no Python interpreter found."
        exit 1
    fi
fi

# Resolve app entrypoint.
APP_FILE="$SCRIPT_DIR/fixed_app.py"
if [ ! -f "$APP_FILE" ]; then
    echo "Error: application file not found at '$APP_FILE'"
    exit 1
fi

# Default port and auto-fallback if occupied.
PORT=8501
if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "Port $PORT is already in use. Searching for an available port..."
    for candidate in {8502..8510}; do
        if ! lsof -nP -iTCP:"$candidate" -sTCP:LISTEN >/dev/null 2>&1; then
            PORT=$candidate
            break
        fi
    done
fi

echo "Launching app on http://localhost:$PORT"
exec "$PYTHON_EXEC" -m streamlit run "$APP_FILE" --server.port "$PORT"
