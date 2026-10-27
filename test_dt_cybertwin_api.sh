#!/usr/bin/env bash
# DT-CyberTwin API smoke tests
# Run from the repository root with the virtual environment activated.
# Start the API separately in another terminal:
#   uvicorn main:app --app-dir backend --reload
#
# Usage:
#   chmod +x test_api.sh
#   ./test_api.sh
#
# Requires: curl, json_pp (usually provided by perl)

set -u

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"
PASS=0
FAIL=0

pretty_json() {
    # Pretty-print valid JSON; show raw output if the response isn't JSON.
    local body="$1"
    if command -v json_pp >/dev/null 2>&1; then
        printf '%s\n' "$body" | json_pp 2>/dev/null || printf '%s\n' "$body"
    else
        printf '%s\n' "$body"
        echo "NOTE: json_pp not found; install Perl's JSON::PP module or use python -m json.tool."
    fi
}

run_get() {
    local name="$1"
    local path="$2"
    local tmp code body
    tmp="$(mktemp)"
    echo
    echo "============================================================"
    echo "TEST: $name"
    echo "GET ${BASE_URL}${path}"
    code="$(curl -sS -o "$tmp" -w '%{http_code}' "${BASE_URL}${path}")" || {
        echo "FAIL: curl could not reach the API."
        rm -f "$tmp"
        FAIL=$((FAIL + 1))
        return
    }
    body="$(cat "$tmp")"
    rm -f "$tmp"
    echo "HTTP STATUS: $code"
    echo "RESPONSE:"
    pretty_json "$body"
    if [[ "$code" =~ ^2 ]]; then
        echo "RESULT: PASS (HTTP 2xx)"
        PASS=$((PASS + 1))
    else
        echo "RESULT: FAIL"
        FAIL=$((FAIL + 1))
    fi
}

run_post() {
    local name="$1"
    local payload="$2"
    local expected="$3"
    local tmp code body
    tmp="$(mktemp)"
    echo
    echo "============================================================"
    echo "TEST: $name"
    echo "POST ${BASE_URL}/simulations/industrial-temperature"
    echo "REQUEST:"
    pretty_json "$payload"
    code="$(curl -sS -o "$tmp" -w '%{http_code}' \
        -X POST "${BASE_URL}/simulations/industrial-temperature" \
        -H 'Content-Type: application/json' \
        --data "$payload")" || {
        echo "FAIL: curl could not reach the API."
        rm -f "$tmp"
        FAIL=$((FAIL + 1))
        return
    }
    body="$(cat "$tmp")"
    rm -f "$tmp"
    echo "HTTP STATUS: $code"
    echo "RESPONSE:"
    pretty_json "$body"

    if [[ "$code" == "$expected" ]]; then
        echo "RESULT: PASS (expected HTTP $expected)"
        PASS=$((PASS + 1))
    else
        echo "RESULT: FAIL (expected HTTP $expected, got $code)"
        FAIL=$((FAIL + 1))
    fi
}

echo "DT-CyberTwin API smoke tests"
echo "Base URL: $BASE_URL"
echo "Make sure the API is running in another terminal."
if ! curl -sS --connect-timeout 2 "${BASE_URL}/health" >/dev/null; then
    echo "ERROR: API is not reachable at ${BASE_URL}."
    echo "Start it with: uvicorn main:app --app-dir backend --reload"
    exit 2
fi

# 1. Health endpoint
run_get "Health endpoint" "/health"

# 2. Digital twin graph
run_get "Digital twin graph endpoint" "/twin"

# 3. Baseline simulation (no attack)
run_post "Baseline industrial-temperature simulation" \
'{
  "steps": 12,
  "attack": false,
  "initial_temperature": 25,
  "setpoint": 40
}' "200"

# 4. Sensor-spoofing simulation
run_post "Sensor-spoofing attack simulation" \
'{
  "steps": 12,
  "attack": true,
  "attack_timestep": 2,
  "spoof_offset": -30,
  "initial_temperature": 25,
  "setpoint": 40
}' "200"

# 5. Invalid attack timestep should be rejected
run_post "Invalid attack timestep validation" \
'{
  "steps": 3,
  "attack": true,
  "attack_timestep": 9,
  "spoof_offset": -30,
  "initial_temperature": 25,
  "setpoint": 40
}' "422"

echo
echo "============================================================"
echo "SUMMARY: ${PASS} passed, ${FAIL} failed"
if (( FAIL > 0 )); then
    exit 1
fi
exit 0
