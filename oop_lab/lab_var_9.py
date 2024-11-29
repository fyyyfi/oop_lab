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
