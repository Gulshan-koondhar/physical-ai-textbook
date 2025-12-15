import time
from typing import Dict
from fastapi import Request, HTTPException
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_size: int = 60):
        """
        Initialize rate limiter
        :param max_requests: Maximum number of requests allowed
        :param window_size: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_size = window_size
        self.requests: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request from identifier is allowed
        :param identifier: Unique identifier for the requester (e.g., IP address)
        :return: True if allowed, False otherwise
        """
        current_time = time.time()

        # Remove requests outside the current window
        while (self.requests[identifier] and
               current_time - self.requests[identifier][0] > self.window_size):
            self.requests[identifier].popleft()

        # Check if we've exceeded the limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False

        # Add current request
        self.requests[identifier].append(current_time)
        return True

# Create a global rate limiter instance
rate_limiter = RateLimiter(max_requests=30, window_size=60)  # 30 requests per minute per IP

async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to implement rate limiting
    """
    # Get client IP address
    client_ip = request.client.host

    # Check if request is allowed
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    response = await call_next(request)
    return response