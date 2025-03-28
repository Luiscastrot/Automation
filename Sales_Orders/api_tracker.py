import time
import json
import threading

# File-based persistence for API usage
TRACKER_FILE = "api_usage.json"
LOCK = threading.Lock()  # Prevent race conditions in multithreading

def initialize_tracker():
    """Initialize the tracker file if it doesn't exist."""
    print("Initializing tracker...")
    with LOCK:
        try:
            with open(TRACKER_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize tracker with timestamps
            now = time.time()
            data = {
                "api_calls": 0,
                "minute_calls": 0,
                "hour_calls": 0,
                "last_reset": now,
                "last_minute_reset": now,
                "last_hour_reset": now,
            }
            with open(TRACKER_FILE, "w") as f:
                json.dump(data, f)

def log_api_call():
    """Log an API call and enforce limits."""
    initialize_tracker()
    
    with LOCK:
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)

        now = time.time()
        
        # Check if API call limits are being reached
        print(f"Checking API limits at {now}...")
        
        # Reset counters if limits exceeded
        if now - data["last_reset"] >= 86400:  # Reset daily limit after 24h
            data["api_calls"] = 0
            data["last_reset"] = now

        if now - data["last_minute_reset"] >= 60:  # Reset minute limit every 60s
            data["minute_calls"] = 0
            data["last_minute_reset"] = now

        if now - data["last_hour_reset"] >= 3600:  # Reset hourly limit every hour
            data["hour_calls"] = 0
            data["last_hour_reset"] = now

        # Check rate limits
        if data["api_calls"] >= 5000:
            print("Daily API limit reached. Sleeping for 1 hour...")
            time.sleep(3600)
            return False
        
        if data["minute_calls"] >= 60:
            print("Minute API limit reached. Sleeping for 1 minute...")
            time.sleep(60)
            return False

        # Increment counters and save data
        data["api_calls"] += 1
        data["minute_calls"] += 1
        data["hour_calls"] += 1

        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f)

        # Ensure we don't exceed 3 calls per second
        print(f"API Call Count: {data['api_calls']} (Minute: {data['minute_calls']}, Hour: {data['hour_calls']})")
        
        # Sleep for 1 second to avoid exceeding rate limit (3 calls per second)
        time.sleep(1)
        
        return True  # Indicate success

def get_api_usage():
    """Get current API usage."""
    initialize_tracker()
    with open(TRACKER_FILE, "r") as f:
        return json.load(f)

def reset_tracker():
    """Reset the tracker manually if needed."""
    with LOCK:
        now = time.time()
        data = {
            "api_calls": 0,
            "minute_calls": 0,
            "hour_calls": 0,
            "last_reset": now,
            "last_minute_reset": now,
            "last_hour_reset": now,
        }
        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f)

def main():
    # Sample usage
    print("Starting the tracker script...")
    initialize_tracker()
    result = log_api_call()
    if result:
        print("API call logged successfully.")
    else:
        print("API call limit reached.")

    # Get current usage
    usage = get_api_usage()
    print(f"Current API usage: {usage}")

    # Reset tracker if needed
    # reset_tracker()  # Uncomment this if you want to reset the tracker manually

if __name__ == "__main__":
    main()
