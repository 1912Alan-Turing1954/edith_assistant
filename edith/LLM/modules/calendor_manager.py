import calendar
from datetime import datetime
import dateparser
import json
import os

class SimpleCalendar:
    def __init__(self, filename='events.json'):
        self.events = {}
        self.filename = filename
        self.load_events()

    def load_events(self):
        """Load events from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.events = json.load(file)

    def save_events(self):
        """Save events to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.events, file)

    def add_event(self, date, event, time):
        """Add an event to a specific date with time."""
        if date in self.events:
            self.events[date].append({"event": event, "time": time})
        else:
            self.events[date] = [{"event": event, "time": time}]
        print(f"Event: '{event}' added on {date}. Time: {time}.")
        self.save_events()

    def view_events(self, date):
        """View events for a specific date."""
        if date in self.events:
            print(f"Events on {date}:")
            for event in self.events[date]:
                print(f"- Event: {event['event']}, Time: {event['time']}")
        else:
            print(f"No events found on {date}.")

    def parse_event(self, sentence):
        """Parse a natural language sentence to extract date, time, and event description."""
        date_time = dateparser.parse(sentence)
        if date_time:
            formatted_date = date_time.strftime("%Y-%m-%d")
            formatted_time = date_time.strftime("%H:%M")
            event_description = sentence.split("next")[0].strip() if "next" in sentence else sentence.strip()
            self.add_event(formatted_date, event_description, formatted_time)
        else:
            print("Could not understand the date or time. Please specify it differently.")

    def delete_event(self, date, event):
        """Delete an event from a specific date."""
        if date in self.events:
            for e in self.events[date]:
                if e['event'] == event:
                    self.events[date].remove(e)
                    print(f"Event '{event}' removed from {date}.")
                    if not self.events[date]:  # Remove the date entry if no events are left
                        del self.events[date]
                    self.save_events()
                    return
            print(f"Event '{event}' not found on {date}.")
        else:
            print(f"No events found on {date}.")

    def main(self):
        print("Welcome to the Advanced Calendar! Type your events or 'exit' to quit.")
        while True:
            sentence = input("Enter event: ")
            if sentence.lower() == 'exit':
                print("Exiting the calendar app.")
                break
            elif sentence.lower().startswith("delete "):
                _, event = sentence.split("delete ", 1)
                date_str = input("Enter the date for deletion (YYYY-MM-DD): ")
                self.delete_event(date_str, event.strip())
            else:
                self.parse_event(sentence)

if __name__ == "__main__":
    calendar_app = SimpleCalendar()
    calendar_app.main()
