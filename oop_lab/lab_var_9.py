from datetime import datetime, timedelta
import random
import json
from typing import List

# Базові класи
class Character:
    def __init__(self, name: str, role: str, age: int = 30, gender: str = "Unknown"):
        self.__name = name
        self.__role = role
        self.__age = age
        self.__gender = gender

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value


class Protagonist(Character):
    def __init__(self, name: str, role: str, motivation: str, age: int = 30, gender: str = "Unknown"):
        super().__init__(name, role, age, gender)
        self.__motivation = motivation


class Antagonist(Character):
    def __init__(self, name: str, role: str, conflict_reason: str, age: int = 30, gender: str = "Unknown"):
        super().__init__(name, role, age, gender)
        self.__conflict_reason = conflict_reason


class Location:
    def __init__(self, name: str, description: str, climate: str = "Moderate"):
        self.__name = name
        self.__description = description
        self.__climate = climate

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description


class UrbanLocation(Location):
    def __init__(self, name: str, description: str, population: int, climate: str = "Moderate"):
        super().__init__(name, description, climate)
        self.__population = population


class RuralLocation(Location):
    def __init__(self, name: str, description: str, agricultural_type: str, climate: str = "Moderate"):
        super().__init__(name, description, climate)
        self.__agricultural_type = agricultural_type


# Класи подій
class Event:
    def __init__(self, title: str, location: Location, participants: List[Character], timestamp: datetime,
                 is_alternative=False, importance_level=1):
        self.__title = title
        self.__location = location
        self.__participants = participants
        self.__timestamp = timestamp
        self.__is_alternative = is_alternative
        self.__importance_level = importance_level

    @property
    def title(self):
        return self.__title

    @property
    def location(self):
        return self.__location

    @property
    def participants(self):
        return self.__participants

    @property
    def timestamp(self):
        return self.__timestamp

    def execute(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def __str__(self):
        participants_names = ", ".join([p.name for p in self.__participants])
        return f"{self.__timestamp}: {self.__title} at {self.__location.name} with {participants_names}"


class FightEvent(Event):
    def execute(self):
        return f"Бій починається між {self.participants[0].name} і {self.participants[1].name}."


class DialogueEvent(Event):
    def execute(self):
        return f"{self.participants[0].name} і {self.participants[1].name} ведуть діалог."


class MonologueEvent(Event):
    def execute(self):
        return f"{self.participants[0].name} розмірковує про своє життя."


# Функції для перевірки й моделювання
def check_character_availability(character: Character, events: List[Event], new_event_time: datetime):
    for event in events:
        if character in event.participants and event.timestamp == new_event_time:
            return False
    return True


def validate_event_reality(event: Event, events: List[Event]):
    for participant in event.participants:
        if not check_character_availability(participant, events, event.timestamp):
            return False
    return True


def generate_alternative_event(original_event: Event):
    new_title = f"Alternative: {original_event.title}"
    new_location = original_event.location
    new_participants = original_event.participants[::-1]  # Інвертуємо список учасників
    new_timestamp = original_event.timestamp + timedelta(days=1)
    return Event(new_title, new_location, new_participants, new_timestamp, is_alternative=True)


# Генерація випадкової події
def generate_random_character():
    roles = ["Protagonist", "Antagonist", "Side Character"]
    name = f"Character_{random.randint(1, 100)}"
    role = random.choice(roles)
    return Character(name, role)


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
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
    if title == "Бій":
        return FightEvent(title, location, participants, timestamp)
    elif title == "Діалог":
        return DialogueEvent(title, location, participants, timestamp)
    elif title == "Монолог":
        return MonologueEvent(title, location, participants, timestamp)


# Збереження і завантаження подій
def save_to_file(data, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_report(events: List[Event], start_date: datetime, end_date: datetime):
    report = [
        str(event)
        for event in events
        if start_date <= event.timestamp <= end_date
    ]
    return report


# Демонстрація роботи
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

# Відновлення подій
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
start_date = datetime.now() - timedelta(days=15)
end_date = datetime.now()
report = generate_report(loaded_events, start_date, end_date)

print("\nЗвіт за останні 15 днів:")
print("\n".join(report))
