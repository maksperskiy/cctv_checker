from datetime import datetime

from django import template

register = template.Library()


@register.filter(name="calculate_timeline_position", is_safe=True)
def calculate_timeline_position(all_items, created_at):
    # Extract the created_at dates from the formset
    dates = []
    for item in all_items:
        if item and item.created_at:
            try:
                date = item.created_at
                dates.append(date)
            except ValueError:
                continue  # Skip any invalid dates

    if not dates:
        return "0%"  # Return 0% if there are no dates

    # Find the earliest and latest dates
    min_date = min(dates)
    max_date = max(dates)

    # Total time range in seconds
    total_seconds = (max_date - min_date).total_seconds()

    # Calculate the current position as a percentage
    current_seconds = (
        datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S.%f%z") - min_date
    ).total_seconds()

    # Handle the case where all dates are the same
    if total_seconds == 0:
        return (
            "100%"  # All events are at the same time, so give each segment equal width
        )

    # Return the percentage width of this segment
    return f"{(current_seconds / total_seconds) * 100}%"


@register.filter(name="abs")
def abs_filter(value):
    return abs(value)


@register.filter
def range_filter(value):
    """Return a range up to the specified value."""
    return range(value)


@register.filter
def status_color(value):
    status_colors = {
        "ok": "#00FF00",
        "warning": "#FF8C00",
        "error": "#FF0000",
        "offline": "#000000",
        "warning_multiple": "#C16C04",
        "unknown": "#A9A9A9",
        "warning_artifacts": "#A54F0C",
    }
    return status_colors.get(value, "gray")
