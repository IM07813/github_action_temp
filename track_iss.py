import requests
import json
import os
from datetime import datetime, timezone

# --- Call the ISS API (no auth needed, completely free) ---
response = requests.get("http://api.open-notify.org/iss-now.json")
data = response.json()

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
lat = data["iss_position"]["latitude"]
lon = data["iss_position"]["longitude"]

# --- Build the new entry ---
entry = {
    "timestamp_utc": timestamp,
    "latitude": lat,
    "longitude": lon,
    "google_maps": f"https://www.google.com/maps?q={lat},{lon}",
    "speed_kmh": 27600  # ISS travels at ~27,600 km/h constantly
}

print(f"✅ ISS is at: {lat}, {lon}")
print(f"🗺️  View on map: {entry['google_maps']}")

# --- Save latest snapshot (always just 1 entry, the most recent) ---
with open("iss_latest.json", "w") as f:
    json.dump(entry, f, indent=2)

# --- Append to the full history log ---
history = []
if os.path.exists("iss_log.json"):
    with open("iss_log.json", "r") as f:
        history = json.load(f)

history.append(entry)

with open("iss_log.json", "w") as f:
    json.dump(history, f, indent=2)

print(f"📦 Total entries logged: {len(history)}")