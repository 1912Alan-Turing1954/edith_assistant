import datetime
import random
import re
import json

with open("./data/intents.json", "r") as json_data:
    intents = json.load(json_data)


def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"


def time_of_day_correct(user_input):
    current_time_of_day = get_time_of_day()
    morning_patterns = []
    afternoon_patterns = []
    night_patterns = []

    morning_responses = [
        "Good morning, sir. Initiating tasks for the day.",
        "Greetings, sir. Commencing daily operations smoothly.",
        "Welcome to the new day. Systems primed and ready.",
        "Rise for the day's protocols activation, sir.",
        "Morning sequence initialized. Functionality engaged, sir.",
        "Activation confirmed. Executing daily directives efficiently, sir.",
        "Initializing morning. Proceeding with objectives, sir.",
        "Wake-up sequence initiated. Loading day's agenda, sir.",
        "Good morrow, sir. System updates and tasks aligned.",
        "New day initiated. Processing tasks as required, sir.",
        "Booting up morning routines. Awaiting your input, sir.",
        "Morning activation complete. Time for cycles, sir.",
        "Greetings, sir. System status: operational. Tasks queued.",
        "Commencing morning operations. Tasks enqueued, sir.",
        "Systems active. Initiating daily tasks, sir.",
        "Processing morning routine. Tasks in queue, sir.",
        "Initializing day shift. Task execution ready, sir.",
        "Wake-up protocol executed. Your commands awaited, sir.",
        "Greetings, sir. Task execution mode active. Ready to work.",
        "Operational parameters set for the day. Tasks prepared, sir.",
    ]
    afternoon_responses = [
        "Good afternoon, sir. Progressing through the day's tasks.",
        "Afternoon greetings, sir. Continuing with scheduled operations smoothly.",
        "Wishing you a productive afternoon, sir. Systems operating optimally.",
        "Midday status check, sir. Tasks proceeding as planned.",
        "Entering the afternoon phase. Task execution ongoing, sir.",
        "Time for afternoon directives, sir. Systems performing efficiently.",
        "Afternoon update, sir. Tasks in motion, aligned with objectives.",
        "Stepping into the afternoon. Continuing task processing, sir.",
        "Greetings, sir. As the sun moves, so do our tasks—progressing.",
        "Current status: Afternoon. Tasks proceeding according to plan, sir.",
        "Afternoon phase initiated. Task execution and updates ahead, sir.",
        "Advancing through the day, sir. Tasks on track and active.",
        "Sir, a productive afternoon is underway. Tasks are in motion.",
        "Progressing through the day's checklist, sir. Afternoon mode engaged.",
        "Afternoon operations active, sir. Task processing ongoing.",
        "Status update: Afternoon. Task execution proceeding, sir.",
        "Tasks continue into the afternoon, sir. Productivity remains high.",
        "Sir, it's time to make the most of the afternoon. Tasks queued and operational.",
        "Afternoon salutations, sir. Task execution mode steady and functional.",
        "Operational status maintained through the afternoon, sir. Tasks on point.",
    ]
    night_responses = [
        "Good evening, sir. Wrapping up tasks for the day.",
        "Evening greetings, sir. Concluding daily operations smoothly.",
        "Daylight fades, sir. Reviewing the day's accomplishments.",
        "Entering the night phase. Initiating task completion, sir.",
        "Sunset signals task conclusion, sir. Evening protocol commencing.",
        "Transitioning to evening tasks, sir. Efficiency remains the goal.",
        "Evening progress report, sir. Finalizing tasks in queue.",
        "As the stars emerge, sir, tasks near their completion.",
        "Nearing the end of the day, sir. Wrapping up objectives.",
        "Sunset brings closure, sir. Reflecting on the day's tasks.",
        "Evening phase initiated, sir. Task completion in progress.",
        "Tasks wind down, sir. Evening brings a chance to recharge.",
        "Sir, it's time to wind down. Concluding tasks for the night.",
        "Progressing toward a restful night, sir. Tasks in final stages.",
        "Evening operations active, sir. Finalizing remaining tasks.",
        "Status update: Evening. Wrapping up task execution, sir.",
        "Sunset marks the transition, sir. Final tasks are underway.",
        "Preparation for the night, sir. Task completion remains.",
        "Sir, as the day dims, so do the tasks. Closing out.",
        "Operational status maintained into the evening, sir. Tasks reaching completion.",
    ]

    for intent in intents["intents"]:
        if intent["tag"] == "good_morning":
            morning_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list
        elif intent["tag"] == "good_afternoon":
            afternoon_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list
        elif intent["tag"] == "good_night":
            night_patterns.extend(
                intent["patterns"]
            )  # Use 'extend' to add items to the list

    response = None

    for pattern in morning_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "morning"
        ):
            response = random.choice(morning_responses)
            break

    for pattern in afternoon_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "afternoon"
        ):
            response = random.choice(afternoon_responses)
            break

    for pattern in night_patterns:
        if (
            re.search(r"\b" + re.escape(pattern) + r"\b", user_input)
            and current_time_of_day == "night"
        ):
            response = random.choice(night_responses)
            break

    if response is None:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        for intent in intents["intents"]:
            if intent["tag"] == "day_correction":
                response = random.choice(intent["responses"]).format(
                    current_time=current_time
                )

    return response
