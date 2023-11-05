#!/bin/bash

echo "[+] Starting ThreatPulse in Dev mode"
docker compose -f docker/dev/docker-compose.yml up --build