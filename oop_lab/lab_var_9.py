from datetime import datetime, timedelta
import random
import json
from typing import List



class Character:
    def __init__(self, name: str, role: str, age: int, gender: str):
        self.name = name
        self.role = role
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name} ({self.role}, {self.age} років, {self.gender})"


class Protagonist(Character):
    def __init__(self, name: str, role: str, age: int, gender: str, motivation: str):
        super().__init__(name, role, age, gender)
        self.motivation = motivation


class Antagonist(Character):
    def __init__(self, name: str, role: str, age: int, gender: str, conflict_reason: str):
        super().__init__(name, role, age, gender)
        self.conflict_reason = conflict_reason


class Location:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class UrbanLocation(Location):
    def __init__(self, name: str, description: str, population: int):
        super().__init__(name, description)
        self.population = population


class RuralLocation(Location):
    def __init__(self, name: str, description: str, agricultural_type: str):
        super().__init__(name, description)
        self.agricultural_type = agricultural_type


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


# Функції для перевірки реальності подій
def check_event_reality(events: List[Event]) -> bool:
    """
    Перевіряє, чи персонажі не знаходяться в кількох місцях одночасно.
    """
    event_map = {}
    for event in events:
        for participant in event.participants:
            if participant.name in event_map:
                if event_map[participant.name] != event.timestamp:
                    print(f"Помилка: {participant.name} одночасно знаходиться в різних місцях!")
                    return False
            else:
                event_map[participant.name] = event.timestamp
    return True


# Функція для моделювання альтернативних сценаріїв
def generate_alternative_scenario(events: List[Event]):
    new_events = []
    for event in events:
        altered_title = f"Altern: {event.title}"
        altered_timestamp = event.timestamp + timedelta(hours=random.randint(1, 12))
        new_event = Event(
            title=altered_title,
            location=event.location,
            participants=event.participants,
            timestamp=altered_timestamp,
        )
        new_events.append(new_event)
    return new_events


# Збереження і завантаження подій
def save_to_file(data, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# Функція генерації звіту
def generate_report(events: List[Event], start_date: datetime, end_date: datetime, filter_character=None):
    report = []
    for event in events:
        if start_date <= event.timestamp <= end_date:
            if not filter_character or any(p.name == filter_character for p in event.participants):
                report.append(str(event))
    return report


# Демонстрація
characters = [Character("Тайлер", "Антигерой", 30, "чоловік"), Character("Марла", "Партнер", 27, "жінка")]
locations = [
    Location("Бар", "Тихий, темний бар"),
    Location("Підвал", "Місце для бійцівського клубу"),
    Location("Квартира", "Місце проживання Розповідача"),
]
events = [
    FightEvent("Бій", locations[1], [characters[0], characters[1]], datetime.now() - timedelta(days=5)),
    DialogueEvent("Діалог", locations[0], [characters[0], characters[1]], datetime.now() - timedelta(days=10)),
]

# Перевірка правил реальності
if check_event_reality(events):
    print("Усі події відповідають правилам реальності.")

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
        participants=[Character(name, "", 0, "") for name in e["participants"]],
        timestamp=datetime.fromisoformat(e["timestamp"]),
    )
    for e in loaded_event_data
]

# Генерація звіту
start_date = datetime.now() - timedelta(days=15)
end_date = datetime.now()
report = generate_report(loaded_events, start_date, end_date, filter_character="Тайлер")

print("\nЗвіт за останні 15 днів:")
print("\n".join(report))
