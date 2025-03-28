import time
import json

# File-based persistence for API usage
TRACKER_FILE = "api_usage.json"

def initialize_tracker():
    """Initialize the tracker file if it doesn't exist."""
    try:
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Initialize empty tracker
        data = {"api_calls": 0, "last_reset": time.time()}
        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f)

def log_api_call():
    """Log an API call."""
    initialize_tracker()
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)

    # Increment API call count
    data["api_calls"] += 1

    # Save updated data
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f)

    print(f"API Call Count: {data['api_calls']}")

def reset_tracker():
    """Reset the tracker."""
    initialize_tracker()
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)

    # Reset call count and timestamp
    data["api_calls"] = 0
    data["last_reset"] = time.time()

    # Save updated data
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f)

def get_api_usage():
    """Get current API usage."""
    initialize_tracker()
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)
    
    return data
