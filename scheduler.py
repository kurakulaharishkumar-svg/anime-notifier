"""
scheduler.py
Runs the main job on a 1-hour schedule using the `schedule` library.
"""

import schedule
from time import sleep


def start_scheduler(job) -> None:
    """
    Schedule the given job to run every 1 hour, then enter the
    blocking run loop.

    Args:
        job: A callable with no arguments to run on each tick.
    """
    # Run once immediately on startup
    job()

    schedule.every(1).hours.do(job)

    print("[SCHEDULER] Running every 1 hour. Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        sleep(1)
