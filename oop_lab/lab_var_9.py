import random
import json
from typing import List

# Базовий клас персонажа
class Character:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def interact(self, other: "Character"):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def __str__(self):
        return f"{self.name} ({self.role})"
class MainCharacter(Character):
    def interact(self, other: "Character"):
        return f"{self.name} глибоко спілкується з {other.name}."


class SupportingCharacter(Character):
    def interact(self, other: "Character"):
        return f"{self.name} вітає {other.name}."


# Місце
class Location:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.name}: {self.description}"


# Базовий клас події
class Event:
    def __init__(self, title: str, location: Location, participants: List[Character]):
        self.title = title
        self.location = location
        self.participants = participants

    def execute(self):
        raise NotImplementedError("This method should be implemented in subclasses.")

    def __str__(self):
        participants_names = ", ".join([p.name for p in self.participants])
        return f"{self.title} at {self.location.name} with {participants_names}"