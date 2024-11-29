from datetime import datetime, timedelta
import random
import json
from typing import List

# Клас локації
class Location:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.description})"

# Клас персонажа
class Character:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.role})"

# Клас події з часовою міткою
class Event:
    def __init__(self, title: str, location: Location, participants: List[Character], timestamp: datetime):
        self.title = title
        self.location = location
        self.participants = participants
        self.timestamp = timestamp

    def execute(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def __str__(self):
        participants_names = ", ".join([p.name for p in self.participants])
        return f"{self.timestamp}: {self.title} at {self.location.name} with {participants_names}"


class FightEvent(Event):
    def execute(self):
        return f"Бій починається між {self.participants[0].name} і {self.participants[1].name}."


class DialogueEvent(Event):
    def execute(self):
        return f"{self.participants[0].name} і {self.participants[1].name} ведуть діалог."


class MonologueEvent(Event):
    def execute(self):
        return f"{self.participants[0].name} розмірковує про своє життя."


# Генерація випадкової події з часовою міткою
def generate_random_event():
    titles = ["Зустріч", "Бій", "Діалог", "Монолог"]
    locations = [
        Location("Бар", "Тихий, темний бар"),
        Location("Підвал", "Місце для бійцівського клубу"),
        Location("Квартира", "Місце проживання Розповідача"),
    ]
    title = random.choice(titles)
    location = random.choice(locations)
    participants = [generate_random_character(), generate_random_character()]
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30))  # Дата події в межах останнього місяця
    if title == "Бій":
        return FightEvent(title, location, participants, timestamp)
    elif title == "Діалог":
        return DialogueEvent(title, location, participants, timestamp)
    elif title == "Монолог":
        return MonologueEvent(title, location, participants, timestamp)


# Клас для генерації персонажів
def generate_random_character():
    names = ["Розповідач", "Тайлер", "Марла", "Боб"]
    roles = ["Головний герой", "Антагоніст", "Антагоніст", "Друг"]
    name = random.choice(names)
    role = random.choice(roles)
    return Character(name, role)


# Збереження і завантаження подій із файлу
def save_to_file(data, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# Функція генерації звіту
def generate_report(events: List[Event], start_date: datetime, end_date: datetime):
    report = [
        str(event)
        for event in events
        if start_date <= event.timestamp <= end_date
    ]
    return report


# Демонстрація
characters = [generate_random_character() for _ in range(5)]
events = [generate_random_event() for _ in range(10)]

# Збереження у файл
event_data = [
    {
        "title": e.title,
        "location": e.location.name,
        "participants": [p.name for p in e.participants],
        "timestamp": e.timestamp.isoformat(),
    }
    for e in events
]
save_to_file(event_data, "events.json")

# Завантаження з файлу
loaded_event_data = load_from_file("events.json")

# Відновлення об'єктів подій із файлу
loaded_events = [
    Event(
        title=e["title"],
        location=Location(e["location"], ""),
        participants=[Character(name, "") for name in e["participants"]],
        timestamp=datetime.fromisoformat(e["timestamp"]),
    )
    for e in loaded_event_data
]

# Генерація звіту
start_date = datetime.now() - timedelta(days=15)  # Останні 15 днів
end_date = datetime.now()
report = generate_report(loaded_events, start_date, end_date)

print("\nЗвіт за останні 15 днів:")
print("\n".join(report))
