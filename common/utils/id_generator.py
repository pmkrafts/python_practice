"""ID generation utilities."""

from uuid import uuid4


def generate_uuid() -> str:
    """Generate a random UUID4 string."""
    return str(uuid4())


def generate_ulid() -> str:
    """Generate a ULID-like string based on timestamp + randomness.

    Note: For true ULIDs use the `ulid-py` package. This is a lightweight fallback.
    """
    import base64
    import time
    import uuid

    timestamp = int(time.time() * 1000).to_bytes(6, "big")
    randomness = uuid.uuid4().bytes[:10]
    return base64.urlsafe_b64encode(timestamp + randomness).decode("ascii").rstrip("=")
