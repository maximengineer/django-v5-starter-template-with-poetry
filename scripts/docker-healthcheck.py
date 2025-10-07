#!/usr/bin/env python
"""Docker health check script with proper error logging."""
import sys
import urllib.request
from datetime import datetime


def log(message):
    """Log messages with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] HEALTHCHECK: {message}", file=sys.stderr, flush=True)


def main():
    """Run health check with error logging."""
    url = "http://localhost:8000/health/"
    timeout = 5

    try:
        log(f"Checking {url} (timeout={timeout}s)")
        resp = urllib.request.urlopen(url, timeout=timeout)

        if resp.status == 200:
            log(f"✓ Health check passed (status={resp.status})")
            sys.exit(0)
        else:
            log(f"✗ Health check failed: unexpected status={resp.status}")
            sys.exit(1)

    except urllib.error.HTTPError as e:
        log(f"✗ HTTP error: {e.code} {e.reason}")
        sys.exit(1)

    except urllib.error.URLError as e:
        log(f"✗ Connection error: {e.reason}")
        sys.exit(1)

    except TimeoutError:
        log(f"✗ Timeout: no response after {timeout}s")
        sys.exit(1)

    except Exception as e:
        log(f"✗ Unexpected error: {type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
