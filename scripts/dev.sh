#!/usr/bin/env bash
set -euo pipefail

trap 'echo "❌ Script failed at line $LINENO"; read -p "Press enter to exit..."' ERR

# Kills any firebase port
cleanup_firebase_ports(){
    echo "Cleaning up old firebase processes...."

    firebase emulators:export ./emulator-data --force || true

    # Kill ALL firebase processes
    pkill -f "firebase" 2>/dev/null || true

    # Kill anyting that uses the emulator ports
    for port in 9099 9199 4000 4500; do
        fuser -k ${port}/tcp 2>/dev/null || true
    done
    # Give OS time to release ports
    sleep 5
}

shutdown(){
    printf "\nStopping services...\n"
    echo "Exporting Firebase emulator data..."

    firebase emulators:export ./emulator-data --force || true

    if [[ -n "${FIREBASE_PID:-}" ]]; then
        kill -INT "${FIREBASE_PID}" 2>/dev/null || true
        wait "$FIREBASE_PID" 2>/dev/null || true
    fi
    docker compose -f compose.dev.yaml down || true
}
trap shutdown EXIT INT TERM

# First clean up all firebase ports if they are open
cleanup_firebase_ports
printf "\nStarting Firebase emulators...\n"

# Starts a new process group
setsid firebase emulators:start \
  --import=./emulator-data \
  --export-on-exit &
FIREBASE_PID=$!

# Wait a bit for Firebase to bind ports
sleep 10
echo "Starting docker container container..."
docker compose -f compose.dev.yaml up --build