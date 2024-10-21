import os
import time

class APIManager:
    def __init__(self):
        self.api_keys = [
            os.getenv("GORQ_API_KEY_1"),
            os.getenv("GORQ_API_KEY_2"),
            # Add more API keys as needed
        ]
        self.current_key_index = 0
        self.requests_made = 0
        self.start_time = time.time()  # Track the start time for rate limiting

    def get_api_key(self):
        return self.api_keys[self.current_key_index]

    def handle_limit(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.requests_made = 0  # Reset requests made with the new key
        print(f"Switched to API Key: {self.get_api_key()}")

    def check_rate_limit(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60:  # Reset every minute
            self.requests_made = 0
            self.start_time = time.time()

        if self.requests_made >= 30:  # Limit to 30 requests per minute
            print("Rate limit reached for this key. Switching key.")
            self.handle_limit()
            return False  # Indicate that we should not proceed with the request
        return True  # Indicate that we can proceed with the request

    def increment_requests(self):
        self.requests_made += 1