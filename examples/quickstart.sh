#!/usr/bin/env bash
# Human-Like AI Tester — 2-minute tour.
set -u
cd "$(dirname "$0")/.." # run from the repo root no matter where invoked

echo "=== 1. Personas (8) ==="
python3 -m human_tester.cli personas | head -n 20

echo "=== 2. Humanize a string (typos + voice + autocorrect + phonetic) ==="
python3 -m human_tester.cli simulate "Lets plan a meeting tomorrow" --voice --autocorrect --phonetic

echo "=== 3. Messy CSV -> validate it ==="
python3 -m human_tester.cli generate-file csv --mixed --output /tmp/messy_human_data.csv
python3 -m human_tester.cli validate-file /tmp/messy_human_data.csv 2>&1 | head -n 25

echo "=== 4. Chatbot vectors (voice mode) + reply evaluation ==="
python3 -m human_tester.cli test-chat --persona impatient_teen --voice --reply "Error 500. Try again." 2>&1 | head -n 30

echo "=== 5. Desktop + mobile heuristic audits ==="
python3 -m human_tester.cli test-desktop "DemoApp" --cancel-distance-px 12 --clipped-at 800 2>&1 | head -n 20
python3 -m human_tester.cli test-mobile "DemoApp" --action-position top-right --keyboard-covered 2>&1 | head -n 20

echo "=== 6. Live demo against the built-in flawed mock app ==="
python3 -m human_tester.cli demo 2>&1 | tail -n 30

echo "=== 7. Unit tests ==="
python3 -m unittest discover -s tests
