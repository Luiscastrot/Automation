import time
import json
import threading

# File-based persistence for API usage per user
TRACKER_FILE = "api_usage.json"
LOCK = threading.Lock()  # Prevent race conditions in multithreading

def initialize_tracker():
    """Initialize the tracker file if it doesn't exist."""
    with LOCK:
        try:
            with open(TRACKER_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize an empty tracker if the file doesn't exist
            data = {}
            with open(TRACKER_FILE, "w") as f:
                json.dump(data, f)

def log_api_call(user_name):
    """Log an API call and enforce limits for a specific user."""
    initialize_tracker()

    with LOCK:
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)

        now = time.time()

        # Initialize the user entry if it doesn't exist
        if user_name not in data:
            data[user_name] = {
                "api_calls": 0,
                "minute_calls": 0,
                "hour_calls": 0,
                "last_reset": now,
                "last_minute_reset": now,
                "last_hour_reset": now,
            }

        user_data = data[user_name]

        # Reset counters if limits exceeded
        if now - user_data["last_reset"] >= 86400:  # Reset daily limit after 24h
            user_data["api_calls"] = 0
            user_data["last_reset"] = now

        if now - user_data["last_minute_reset"] >= 60:  # Reset minute limit every 60s
            user_data["minute_calls"] = 0
            user_data["last_minute_reset"] = now

        if now - user_data["last_hour_reset"] >= 3600:  # Reset hourly limit every hour
            user_data["hour_calls"] = 0
            user_data["last_hour_reset"] = now

        # Check rate limits
        if user_data["api_calls"] >= 5000:
            print(f"Daily API limit reached for {user_name}. Sleeping for 1 hour...")
            time.sleep(3600)
            return False
        
        if user_data["minute_calls"] >= 60:
            print(f"Minute API limit reached for {user_name}. Sleeping for 1 minute...")
            time.sleep(60)
            return False

        # Increment counters and save data
        user_data["api_calls"] += 1
        user_data["minute_calls"] += 1
        user_data["hour_calls"] += 1

        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f)

        # Ensure we don't exceed 3 calls per second
        print(f"API Call Count for {user_name}: {user_data['api_calls']} (Minute: {user_data['minute_calls']}, Hour: {user_data['hour_calls']})")
        
        # Sleep for 1 second to avoid exceeding rate limit (3 calls per second)
        time.sleep(1)
        
        return True  # Indicate success

def get_api_usage(user_name):
    """Get current API usage for a specific user."""
    initialize_tracker()
    with open(TRACKER_FILE, "r") as f:
        data = json.load(f)
        return data.get(user_name, {"api_calls": 0, "minute_calls": 0, "hour_calls": 0})

def reset_tracker(user_name):
    """Reset the tracker manually for a specific user if needed."""
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
        with open(TRACKER_FILE, "r") as f:
            tracker_data = json.load(f)
        
        tracker_data[user_name] = data
        
        with open(TRACKER_FILE, "w") as f:
            json.dump(tracker_data, f)

def main():
    # Sample usage
    print("Starting the tracker script...")

    # Example of using specific usernames for tracking
    user_name = "AlbertRogerUK"  # Set the user for testing

    # Initialize the tracker for the first time
    initialize_tracker()

    # Log an API call for the specific user
    result = log_api_call(user_name)
    if result:
        print("API call logged successfully.")
    else:
        print("API call limit reached.")

    # Get current usage for the specific user
    usage = get_api_usage(user_name)
    print(f"Current API usage for {user_name}: {usage}")

    # Reset tracker if needed for that specific user
    # reset_tracker(user_name)  # Uncomment this if you want to reset the tracker manually

if __name__ == "__main__":
    main()
