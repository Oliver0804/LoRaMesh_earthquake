#!/bin/bash
# Earthquake notification script using API instead of SSH

HOST="192.168.0.148"
PORT="5000"
API_URL="http://${HOST}:${PORT}/send"
CHANNEL=2

# Check if required arguments are provided
if [ $# -lt 2 ]; then
    echo "Error: Missing arguments. Usage: $0 <arg1> <arg2>"
    exit 1
fi

ARG1="$1"
ARG2="$2"
MESSAGE="[LoRa Test]Earthquake ${ARG1} ${ARG2}"
LOGFILE="command_log.txt"
CURRENT_TIME=$(date)

echo "Attempting to connect to ${API_URL}..." >> "${LOGFILE}"
echo "[${CURRENT_TIME}] Sending API request with message: \"${MESSAGE}\" to channel ${CHANNEL}" >> "${LOGFILE}"

# Send API request using curl
RESPONSE=$(curl -s -X POST "${API_URL}" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"${MESSAGE}\", \"channel\": ${CHANNEL}}")

# Check curl exit status
if [ $? -ne 0 ]; then
    echo "API request failed" >> "${LOGFILE}"
    echo "Error: Failed to send API request"
    exit 1
fi

echo "API request sent successfully" >> "${LOGFILE}"
echo "Response: ${RESPONSE}" >> "${LOGFILE}"
echo "" >> "${LOGFILE}"

echo "Message sent successfully: ${MESSAGE}"
echo "Response: ${RESPONSE}"
