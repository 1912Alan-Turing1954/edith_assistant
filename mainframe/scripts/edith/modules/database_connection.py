import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("./mainframe/scripts/data/database/edith_matrix.db")
cursor = conn.cursor()

# Create Models table with Timestamp and Destination
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Models (
        Id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        FilePath TEXT NOT NULL,
        Description TEXT,
        Destination TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
"""
)

# Create Configurations table with Timestamp and Destination
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Configurations (
        Id INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        FilePath TEXT NOT NULL,
        Description TEXT,
        Destination TEXT NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
"""
)

conn.commit()


def insert_model(name, file_path, destination, description=None):
    cursor.execute(
        "INSERT INTO Models (Name, FilePath, Destination, Description) VALUES (?, ?, ?, ?)",
        (name, file_path, destination, description),
    )
    conn.commit()


def insert_configuration(name, file_path, destination, description=None):
    cursor.execute(
        "INSERT INTO Configurations (Name, FilePath, Destination, Description) VALUES (?, ?, ?, ?)",
        (name, file_path, destination, description),
    )
    conn.commit()


# Example usage:
insert_model(
    "Jenny model",
    "./mainframe/scripts/edith/data/database/models/jenny_model/model.pt",
    "unchanged",
    "This is the jenny text to speech model.",
)
insert_configuration(
    "Jenny Configuration",
    "./mainframe/scripts/edith/data/database/models/jenny_model/config.json",
    "unchanged",
    "This is configuration is for text to speech model jenny.",
)

insert_model(
    "Intent model",
    "./mainframe/scripts/edith/data/database/models/intent_model/data.pth",
    "./mainframe/scripts/edith/data/",
    "This is the data model for preforming basic inferences withing the edith_testing file.",
)
insert_configuration(
    "Intent Configuration",
    "./mainframe/scripts/edith/data/database/models/intent_model/intents.json",
    "./edith/data/",
    "This is the configuration/intents for the inents inferences NLP.",
)
insert_configuration(
    "LLM Configuration",
    "./mainframe/scripts/edith/data/database/prompts/boot_personality_prompt.txt",
    "./mainframe/scripts/edith/",
    "This is the configuration for how the LLM should behanve and act.",
)

# print("ello")


def fetch_models():
    cursor.execute(
        "SELECT Id, Name, FilePath, Destination, Description, Timestamp FROM Models"
    )
    rows = cursor.fetchall()
    for row in rows:
        print("Model:", row)


def fetch_configurations():
    cursor.execute(
        "SELECT Id, Name, FilePath, Destination, Description, Timestamp FROM Configurations"
    )
    rows = cursor.fetchall()
    for row in rows:
        print("Configuration:", row)


fetch_configurations()
fetch_models()

conn.close()
