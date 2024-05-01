# lib.py
import os
import resource
import time
import threading

try:
    from recordclass import dataobject
except ImportError:
    class dataobject:
        pass


class Person:
    def __init__(self, firstName: str, lastName: str, age: int):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age

    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def increase_age(self) -> None:
        self.age += 1


class PersonSlots:
    __slots__ = ['firstName', 'lastName', 'age']

    def __init__(self, firstName: str, lastName: str, age: int):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age

    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def increase_age(self) -> None:
        self.age += 1


class PersonDataObject(dataobject):
    __fields__ = ['firstName', 'lastName', 'age']

    def __init__(self, firstName: str, lastName: str, age: int):
        self.firstName = firstName
        self.lastName = lastName
        self.age = age

    def get_full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def increase_age(self) -> None:
        self.age += 1


def create_persons(class_name: str = 'Person', persons_num: int = 1000000) -> None:
    start = time.time()
    Persons = []
    person_class = globals()[class_name]
    for i in range(1, persons_num + 1):
        person = person_class('John', 'Doe', 30)
        person.get_full_name()
        person.increase_age()
        Persons.append(person)
        if i % 1000000 == 0:
            print_stats(start, i)


def print_stats(start: float, objectsCreated: int) -> None:
    elapsed = time.time() - start
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"PID/TID: {os.getpid()}/{threading.get_ident()}, " +
          f"{objectsCreated:,} Objects in {elapsed:.3f} sec / " + 
          f"{memory_usage:.2f} MB")


