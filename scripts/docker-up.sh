#!/usr/bin/env bash
set -euo pipefail

echo "🐳 Starting shared infrastructure via docker-compose..."

cd docker || exit 1

docker-compose up -d

echo "✅ Infrastructure started"
echo ""
echo "Services:"
echo "  PostgreSQL: localhost:5432"
echo "  Redis:      localhost:6379"
echo "  Kafka:      localhost:9092"
echo "  Elasticsearch: localhost:9200"
