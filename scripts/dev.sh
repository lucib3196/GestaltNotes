#!/usr/bin/env bash
set -euo pipefail

trap 'echo "❌ Script failed at line $LINENO"; read -p "Press enter to exit..."' ERR

cleanup_firebase_ports() {
    echo "Cleaning up old firebase processes...."

    firebase emulators:export ./emulator-data

    # Kill ALL firebase processes
    pkill -f "firebase" 2>/dev/null || true

    # Kill anything using emulator ports
    for port in 9099 9199 4000 4500; do
        fuser -k ${port}/tcp 2>/dev/null || true
    done

    sleep 5
}

shutdown() {
    printf "\nStopping services...\n"

    if [[ -n "${FIREBASE_PID:-}" ]]; then
        kill -INT "${FIREBASE_PID}" 2>/dev/null || true
        wait "$FIREBASE_PID" 2>/dev/null || true
    fi

    docker compose -f compose.dev.yaml down || true
}

trap shutdown EXIT INT TERM

cleanup_firebase_ports

printf "\nStarting Firebase emulators...\n"

setsid firebase emulators:start --import=./emulator-data --export-on-exit &

FIREBASE_PID=$!

sleep 10

echo "Starting docker containers..."
docker compose -f compose.dev.yaml up --build