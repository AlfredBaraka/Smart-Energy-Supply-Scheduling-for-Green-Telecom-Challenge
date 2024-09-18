from datetime import datetime, timedelta
import json
import random

# Define the range for simulated usage
usage_min = 3.85
usage_max = 4.62

# Generate data for the past 18 hours including the current hour
current_time = datetime(2024, 9, 18, 10, 0, 0)  # Simulating for today at 10:00 AM
data = []

for i in range(18):
    timestamp = current_time - timedelta(hours=(17 - i))
    usage = round(random.uniform(usage_min, usage_max), 2)
    data.append({
        "user": "user1",
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "usage": usage
    })

# Convert data to JSON format
json_data = json.dumps(data, indent=4)

print(json_data)
