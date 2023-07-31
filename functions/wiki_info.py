import re
import wikipedia

class WikiInfo:
    def __init__(self):
        self.question_patterns = {
            r'who is (.+)': 'summary',
            r'when did (.+) (.+)': 'date',
            r'where was (.+) born': 'birthplace',
            r'what is (.+)': 'summary',
            r'why did (.+) (.+)': 'reason',
            r'how did (.+) (.+)': 'method',
            r'what was (.+)': 'event_summary',
            r'where is (.+)': 'current_location',
            r'how many (.+)': 'quantity',
            r'describe (.+)': 'summary',
            r'define (.+)': 'summary',
            r'who were the (.+)': 'members',  # Question about the members of a group
            r'which (.+) invented (.+)': 'inventor',  # Question about the inventor of something
            r'what are the benefits of (.+)': 'benefits',  # Question about the benefits of something
            r'what are the uses of (.+)': 'uses',  # Question about the uses of something
            r'what are the symptoms of (.+)': 'symptoms',  # Question about the symptoms of a condition
            r'what would happen if (.+)': 'consequences',
            r'what would be the outcome of (.+)': 'consequences',
            r'what happens if (.+)': 'consequences',
            r'what are the results of (.+)': 'consequences',
            r'what are the repercussions of (.+)': 'consequences',
            r'what are the effects of (.+)': 'consequences',
            r'what would occur if (.+)': 'consequences',
            # Add more question patterns as needed
        }

    def _fetch_info_from_wikipedia(self, subject, query_type, action=None):
        try:
            if query_type == 'summary':
                return wikipedia.summary(subject, sentences=2)
            elif query_type == 'event_summary':
                return wikipedia.summary(subject, sentences=3)
            elif query_type == 'date':
                page = wikipedia.page(subject)
                content = page.content
                match = re.search(rf'\b{action}\b(?:.*?)(\d{{4}})', content)
                return f"{action} occurred in {match.group(1)}." if match else f"Sorry, I couldn't find the date for {action}."
            elif query_type == 'birthplace':
                page = wikipedia.page(subject)
                content = page.content
                match = re.search(r'born.*?in\s+([\w\s,.]+)', content, re.IGNORECASE)
                return f"{subject} was born in {match.group(1)}." if match else f"Sorry, I couldn't find the birthplace of {subject}."
            elif query_type == 'reason':
                page = wikipedia.page(subject)
                content = page.content
                match = re.search(rf'\b{action}\b(?:.*?)(because[\w\s,.]+)', content, re.IGNORECASE)
                return f"{action} {match.group(1)}." if match else f"Sorry, I couldn't find the reason for {action}."
            elif query_type == 'method':
                page = wikipedia.page(subject)
                content = page.content
                match = re.search(rf'\b{action}\b(?:.*?)(by[\w\s,.]+)', content, re.IGNORECASE)
                return f"{action} {match.group(1)}." if match else f"Sorry, I couldn't find the method for {action}."
            elif query_type == 'current_location':
                page = wikipedia.page(subject)
                coordinates = page.coordinates
                return f"{subject} is located at latitude {coordinates[0]} and longitude {coordinates[1]}." if coordinates else f"Sorry, I couldn't find the current location of {subject}."
            elif query_type == 'quantity':
                page = wikipedia.page(subject)
                content = page.content
                quantity_match = re.search(r'how many (\w+)', content, re.IGNORECASE)
                return f"There are no specific details available about how many {quantity_match.group(1)} {subject} has." if quantity_match else f"Sorry, I couldn't find any information about how many {subject} has."
            elif query_type == 'consequences':
                page = wikipedia.page(subject)
                content = page.content
                match = re.search(rf'\b{action}\b(?:.*?)(consequences[\w\s,.]+)', content, re.IGNORECASE)
                return f"The consequences of {action} are {match.group(1)}." if match else f"Sorry, I couldn't find the consequences of {action}."
        except wikipedia.exceptions.DisambiguationError as e:
            return f"There are multiple results for '{subject}'. Please specify the subject more precisely."
        except wikipedia.exceptions.PageError as e:
            return f"Sorry, I couldn't find any information about '{subject}'."
        except Exception as e:
            return f"Oops! Something went wrong. Error: {e}"

    def get_info(self, command):
        found_question = False
        for pattern, q_type in self.question_patterns.items():
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                found_question = True
                subject = match.group(1)
                action = match.group(2) if len(match.groups()) > 1 else None
                info = self._fetch_info_from_wikipedia(subject, q_type, action=action)
                if info:
                    print(info)
                    # Assuming there's a function called talk() to read the information aloud
                    # talk(info)
                break

        if not found_question:
            print("I'm sorry, I couldn't understand the question.")

wiki = WikiInfo()



