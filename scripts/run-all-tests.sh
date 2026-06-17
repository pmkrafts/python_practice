#!/usr/bin/env bash
set -euo pipefail

echo "🧪 Running all tests..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    # shellcheck source=/dev/null
    source .venv/bin/activate
fi

# Run common tests first
echo "🧪 Running common tests..."
pytest common/tests -v

# Run phase tests if they exist
for phase in phase-01-fundamentals phase-02-backend-systems phase-03-ai-agents; do
    if [ -d "$phase" ] && find "$phase" -name "test_*.py" -o -name "*_test.py" | grep -q .; then
        echo "🧪 Running $phase tests..."
        pytest "$phase" -v
    else
        echo "⏭️  No tests found in $phase"
    fi
done

echo "✅ All tests completed"
