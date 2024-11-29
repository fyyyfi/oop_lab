"""abc: це стандартна бібліотека Python для створення абстрактних класів. ABC — це базовий клас для абстрактних класів, а abstractmethod використовується для визначення абстрактних методів, які мають бути реалізовані в підкласах.
typing: бібліотека, яка дозволяє працювати з типами в Python, особливо для підтримки типізації та generics.
Generic: це клас для оголошення шаблонів типів (generics).
TypeVar: дозволяє створювати універсальні типи (наприклад, для списків, які можуть містити елементи різних типів).
Callable: тип, що описує функцію або метод.
Optional: означає, що значення може бути певного типу або None."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Callable, Optional

T = TypeVar('T') 

class BaseList(ABC, Generic[T]):
    
    
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


class Node(Generic[T]):
    def __init__(self, value: T, next_node: Optional['Node[T]'] = None):
        self.value = value
        self.next = next_node


class LinkedList(BaseList[T]):
    def __init__(self):
        self.head: Optional[Node[T]] = None
        self.size = 0

    def append(self, value: T) -> None:
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def find_by_value(self, value: T) -> Optional[int]:
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return None

    def find_by_index(self, index: int) -> Optional[T]:
        if index < 0 or index >= self.size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value if current else None

    def find_first_by_condition(self, condition: Callable[[T], bool]) -> Optional[T]:
        current = self.head
        while current:
            if condition(current.value):
                return current.value
            current = current.next
        return None

    def __len__(self) -> int:
        return self.size

class CircularLinkedList(LinkedList[T]):
    def append(self, value: T) -> None:
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
        self.size += 1

#Реалізація XORLinkedList
import ctypes

class XORNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.both = 0  


class XORLinkedList(BaseList[T]):
    def __init__(self):
        self.head: Optional[XORNode[T]] = None
        self.tail: Optional[XORNode[T]] = None
        self.size = 0

    def _xor(self, a: Optional[XORNode[T]], b: Optional[XORNode[T]]) -> int:
        return (id(a) if a else 0) ^ (id(b) if b else 0)

    def _get_node_by_id(self, node_id: int) -> Optional[XORNode[T]]:
        return ctypes.cast(node_id, ctypes.py_object).value if node_id else None

    def append(self, value: T) -> None:
        new_node = XORNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.both = id(self.tail)
            self.tail.both ^= id(new_node)
            self.tail = new_node
        self.size += 1

    def find_by_index(self, index: int) -> Optional[T]:
        if index < 0 or index >= self.size:
            return None
        prev_id = 0
        current = self.head
        for _ in range(index):
            next_id = prev_id ^ current.both
            prev_id = id(current)
            current = self._get_node_by_id(next_id)
        return current.value if current else None

    def find_by_value(self, value: T) -> Optional[int]:
        prev_id = 0
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            next_id = prev_id ^ current.both
            prev_id = id(current)
            current = self._get_node_by_id(next_id)
            index += 1
        return None




class VList(BaseList[T]):
    def __init__(self):
        self.levels = [[]]
        self.size = 0

    def append(self, value: T) -> None:
        if not self.levels[-1]:
            self.levels[-1].append(value)
        elif len(self.levels[-1]) == len(self.levels) * len(self.levels):
            self.levels.append([])
        self.levels[-1].append(value)
        self.size += 1

if __name__ == "__main__":
    # Примітивні типи
    int_list = LinkedList[int]()
    int_list.append(10)
    int_list.append(20)
    print("Find value 10 in int list:", int_list.find_by_value(10))  # Output: 0

    float_list = LinkedList[float]()
    float_list.append(10.5)
    float_list.append(20.75)
    print("Find value 20.75 in float list:", float_list.find_by_value(20.75))  # Output: 1

    # Бібліотечні типи
    str_list = LinkedList[str]()
    str_list.append("apple")
    str_list.append("banana")
    print("Find value 'banana' in string list:", str_list.find_by_value("banana"))  # Output: 1

    vector_list = LinkedList[list]()
    vector_list.append([1, 2, 3])
    vector_list.append([4, 5, 6])
    print("Find value [4, 5, 6] in vector list:", vector_list.find_by_value([4, 5, 6]))  # Output: 1

    # Користувацький клас
    class CustomClass:
        def __init__(self, name: str):
            self.name = name

    custom_list = LinkedList[CustomClass]()
    custom_list.append(CustomClass("Example"))
    print("Find CustomClass with name 'Example':", custom_list.find_first_by_condition(lambda x: x.name == "Example").name)  # Output: Example
