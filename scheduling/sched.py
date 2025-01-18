#!/usr/bin/env python3

from datetime import datetime, timedelta
import sys

# Define ANSI color codes
COLORS = {
    "purple": "\033[95m",
    "brown": "\033[33m",
    "maroon": "\033[31m",
    "blue": "\033[94m",
    "red": "\033[91m",
    "green": "\033[92m",
    "reset": "\033[0m"
}

def find_matching_event(reference_event, schedule):
    """
    Finds the best matching event in the schedule, ignoring case and allowing partial matches.
    Returns the full event name if found, None if no match or multiple matches.
    """
    reference_event = reference_event.lower().strip("'\"")
    matches = []
    
    for event, _, _ in schedule:
        if reference_event in event.lower():
            matches.append(event)
    
    if len(matches) == 1:
        return matches[0]
    elif len(matches) == 0:
        print("\nNo matching events found. Here are all possible events:")
        for event, _, _ in schedule:
            print(f"- {event}")
        return None
    else:
        print("\nMultiple matching events found:")
        for match in matches:
            print(f"- {match}")
        return None

def adjust_schedule(reference_time, reference_event, schedule):
    """
    Adjusts the schedule based on a reference time and event.
    """
    # Parse the reference time
    ref_time = datetime.strptime(reference_time, "%H:%M")
    
    # Remove quotes if present in reference_event
    reference_event = find_matching_event(reference_event, schedule)
    
    # Find the index of the reference event
    reference_index = None
    for i, (event, duration, start_time) in enumerate(schedule):
        if event.lower() == reference_event.lower():
            reference_index = i
            break
            
    if reference_index is None:
        print("\nReference event not found. Here are all possible events:")
        for event, _, _ in schedule:
            print(f"- {event}")
        raise ValueError(f"\nPlease choose one of the events listed above.")
    
    # Calculate the difference between reference time and the current start time
    current_start_time = datetime.strptime(schedule[reference_index][2], "%H:%M")
    time_difference = ref_time - current_start_time
    
    # Adjust all times in the schedule based on the time difference
    adjusted_schedule = []
    for event, duration, start_time in schedule:
        start_time_dt = datetime.strptime(start_time, "%H:%M")
        adjusted_start_time = start_time_dt + time_difference
        adjusted_schedule.append((event, duration, adjusted_start_time.strftime("%H:%M")))
    
    return adjusted_schedule


def print_schedule(schedule):
    """
    Prints the schedule in a readable format with color coding.
    """
    print("Daily Schedule:")
    for event, duration, start_time in schedule:
        end_time = (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=duration)).strftime("%H:%M")
        color = get_event_color(event)
        print(f"{color}{start_time} - {end_time}: {event}{COLORS['reset']}")


def get_event_color(event):
    """
    Returns the appropriate color for the event.
    """
    event_lower = event.lower()
    if "study session" in event_lower or "final review" in event_lower:
        return COLORS["purple"]
    elif "plan the day" in event_lower:
        return COLORS["brown"]
    elif "workout" in event_lower:
        return COLORS["maroon"]
    elif "nap" in event_lower:
        return COLORS["green"]
    elif any(keyword in event_lower for keyword in ["wake up", "morning routine", "lunch", "dinner"]):
        return COLORS["blue"]
    else:
        return COLORS["red"]


# Default schedule: List of tuples (event, duration in minutes, start time)
schedule = [
    ("Wake Up and Morning Routine", 15, "07:00"),  # Starts at 07:00, ends at 07:15
    ("Plan the Day", 15, "07:15"),                # Starts at 07:15, ends at 07:30
    ("Deep Study Session 1", 120, "07:30"),       # Starts at 07:30, ends at 09:30
    ("Break", 15, "09:30"),                       # Starts at 09:30, ends at 09:45
    ("Deep Study Session 2", 120, "09:45"),       # Starts at 09:45, ends at 11:45
    ("Nap", 30, "11:45"),                       # Starts at 11:45, ends at 12:15
    ("Study Session 3", 120, "12:15"),            # Starts at 12:15, ends at 14:15
    ("Break", 15, "14:15"),                       # Starts at 14:15, ends at 14:30
    ("Study Session 4", 120, "14:30"),            # Starts at 14:30, ends at 16:30
    ("Workout", 90, "16:30"),                     # Starts at 16:30, ends at 18:00
    ("Study Session 5", 120, "18:00"),            # Starts at 18:00, ends at 20:00
    ("Wind Down", 30, "20:00"),                   # Starts at 20:00, ends at 20:30
    ("Study Session 6", 120, "20:30"),            # Starts at 18:00, ends at 20:00
    ("Anki Cards", 30, "22:30")                   # Starts at 20:30, ends at 21:00
]

# Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <reference_time> <reference_event>")
    print("Example: python script.py 6:00 'Wake Up'")
    sys.exit(1)

# Get arguments from the command line
reference_time = sys.argv[1]
reference_event = sys.argv[2]

# Adjust and print the schedule
try:
    adjusted_schedule = adjust_schedule(reference_time, reference_event, schedule)
    print_schedule(adjusted_schedule)
except ValueError as e:
    print(e)
