from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Optional

T = TypeVar('T')  # Узагальнений тип для підтримки будь-яких даних

class BaseList(ABC, Generic[T]):
    """Абстрактний базовий клас для списків."""
    
    @abstractmethod
    def append(self, value: T) -> None:
        """Додає елемент до списку."""
        pass

    @abstractmethod
    def find_by_value(self, value: T) -> Optional[int]:
        """Шукає індекс першого елемента за заданим значенням."""
        pass

    @abstractmethod
    def find_by_index(self, index: int) -> Optional[T]:
        """Знаходить елемент за індексом."""
        pass

    @abstractmethod
    def find_first_by_condition(self, condition: Callable[[T], bool]) -> Optional[T]:
        """Шукає перший елемент, що відповідає заданій умові."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Повертає розмір списку."""
        pass

