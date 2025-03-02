from django.shortcuts import render
from django.utils.timezone import now
from datetime import timedelta
from collections import defaultdict
from .models import Check


def dashboard_callback(request, context):
    today = now().date()
    start_date = today - timedelta(days=183)

    # Dictionary to store status counts per day
    status_data = defaultdict(lambda: defaultdict(int))

    # Fetch all checks within the date range
    checks = Check.objects.filter(created_at__date__gte=start_date)

    for check in checks:
        check_date = check.created_at.date()
        status_data[check_date][check.status.lower()] += 1

    # Define the color mappings
    status_colors = {
        Check.OK.lower(): "#00FF00",
        Check.WARNING.lower(): "#FF8C00",
        Check.OFFLINE.lower(): "#000000",
        Check.ERROR.lower(): "#FF0000",
        Check.UNKNOWN.lower(): "#A9A9A9",
        Check.WARNING_MULTIPLE.lower(): "#C14309",
    }

    # Prepare data with computed color for each day
    calendar_stats = []
    calendar_weeks = []
    for single_date in (start_date + timedelta(n) for n in range((today - start_date).days + 1)):
        status_counts = status_data[single_date]
        if status_counts:
            avg_status = max(status_counts, key=status_counts.get)
        else:
            avg_status = 'unknown'  # Default to 'unknown' if no checks for the day
        calendar_weeks.append(single_date.isocalendar().week)

        calendar_stats.append({
            'date': single_date,
            'status': avg_status,
            'color': status_colors[avg_status]  # Get the color directly
        })
        calendar_weeks.append(single_date.isocalendar().week)

    context.update({
        'calendar_stats': calendar_stats,
        'weeks_count': max(calendar_weeks) - min(calendar_weeks) + 1,
    })

    return context
