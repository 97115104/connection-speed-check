#!/usr/bin/env python3
"""Simple internet speed check for the current connection.

This script downloads a sample payload from Cloudflare's speed endpoint and
prints an approximate download speed. It uses only the Python standard library.
"""

import argparse
import statistics
import time
import urllib.request


DEFAULT_URL = "https://speed.cloudflare.com/__down?bytes=25000000"


def measure_download(url: str, runs: int) -> list[float]:
    speeds = []
    for run in range(1, runs + 1):
        started = time.perf_counter()
        bytes_read = 0
        request = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(request, timeout=60) as response:
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                bytes_read += len(chunk)

        elapsed = max(time.perf_counter() - started, 0.001)
        mbps = (bytes_read * 8) / elapsed / 1_000_000
        speeds.append(mbps)
        print(f"Run {run}: {mbps:.2f} Mbps over {elapsed:.2f}s")
    return speeds


def main() -> None:
    parser = argparse.ArgumentParser(description="Check approximate internet download speed.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Download URL to test against")
    parser.add_argument("--runs", type=int, default=3, help="Number of test runs")
    args = parser.parse_args()

    speeds = measure_download(args.url, max(args.runs, 1))
    print("")
    print(f"Average: {statistics.mean(speeds):.2f} Mbps")
    print(f"Best:    {max(speeds):.2f} Mbps")


if __name__ == "__main__":
    main()
