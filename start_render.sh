#!/bin/bash
set -e

echo "🚀 Starting Letta AI Server on Render..."

# Set default values if not provided
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8283}"
export LETTA_DIR="${LETTA_DIR:-/tmp/letta}"

# Ensure Letta directory exists
echo "📁 Creating Letta directory: $LETTA_DIR"
mkdir -p "$LETTA_DIR/logs"

# Validate required environment variables
if [ -z "$LETTA_PG_URI" ]; then
    echo "❌ Error: LETTA_PG_URI environment variable is required"
    exit 1
fi

echo "🔍 Database URI: ${LETTA_PG_URI}"
echo "🌐 Server will start on: ${HOST}:${PORT}"

# Run database migrations
echo "🔄 Running database migrations..."
if ! alembic upgrade head; then
    echo "❌ Database migration failed! Please check your database connection."
    exit 1
fi
echo "✅ Database migrations completed successfully"

# Start the Letta server with secure mode for ADE integration
echo "🚀 Starting Letta AI Server with ADE support..."
exec python -m letta.main server --host "$HOST" --port "$PORT" --secure