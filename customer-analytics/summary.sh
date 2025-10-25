#!/bin/bash
# summary.sh
# Usage: ./summary.sh <container_name>
if [ -z "$1" ]; then
  echo "Usage: ./summary.sh <container_name>"
  exit 1
fi

CONTAINER_NAME=$1
HOST_RESULTS_DIR="./customer-analytics/results"
CONTAINER_RESULTS_DIR="/app/pipeline/results"

# create host dir
mkdir -p "$HOST_RESULTS_DIR"

echo "Copying results from container $CONTAINER_NAME..."
docker cp "${CONTAINER_NAME}:${CONTAINER_RESULTS_DIR}/." "$HOST_RESULTS_DIR/"

echo "Stopping container $CONTAINER_NAME..."
docker stop "$CONTAINER_NAME" || true



echo "Results copied to $HOST_RESULTS_DIR"
