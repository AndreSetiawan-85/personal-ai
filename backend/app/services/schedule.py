from datetime import datetime, timedelta


class ScheduleError(ValueError):
    pass


def calculate_next_run(
    schedule: str | None,
    from_time: datetime,
) -> datetime | None:
    """
    Calculate the next execution time for a task.

    Supported schedules:
        once
        every:60s
        every:5m
        every:1h
        every:1d

    Returns:
        datetime for the next run,
        or None when the task should not run again.
    """

    if schedule is None:
        return None

    schedule = schedule.strip().lower()

    if not schedule:
        return None

    if schedule == "once":
        return None

    if not schedule.startswith("every:"):
        raise ScheduleError(
            f"Unsupported schedule: {schedule}"
        )

    value = schedule.removeprefix("every:").strip()

    if not value:
        raise ScheduleError(
            "Schedule interval is required."
        )

    unit = value[-1]
    number = value[:-1]

    try:
        amount = int(number)
    except ValueError:
        raise ScheduleError(
            f"Invalid schedule interval: {value}"
        )

    if amount <= 0:
        raise ScheduleError(
            "Schedule interval must be greater than zero."
        )

    if unit == "s":
        delta = timedelta(seconds=amount)

    elif unit == "m":
        delta = timedelta(minutes=amount)

    elif unit == "h":
        delta = timedelta(hours=amount)

    elif unit == "d":
        delta = timedelta(days=amount)

    else:
        raise ScheduleError(
            f"Unsupported schedule unit: {unit}"
        )

    return from_time + delta