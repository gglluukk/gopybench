#cython: language_level=3

import os
import resource
import time
import threading
from libc.stdlib cimport malloc, free

cdef extern from "Python.h":
    object PyDict_New()
    object PyDict_SetItemString(object dict, char* key, object value)
    object Py_BuildValue(char *format, ...)

cdef class Person:
    cdef public str first_name
    cdef public str last_name
    cdef public int age

    def __cinit__(self, bytes first_name, bytes last_name, int age):
        self.first_name = first_name.decode('utf-8')
        self.last_name = last_name.decode('utf-8')
        self.age = age

    cpdef str get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    cpdef increase_age(self):
        self.age += 1

cdef class PersonSlots:
    cdef public str first_name
    cdef public str last_name
    cdef public int age

    def __cinit__(self, bytes first_name, bytes last_name, int age):
        self.first_name = first_name.decode('utf-8')
        self.last_name = last_name.decode('utf-8')
        self.age = age

    cpdef str get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    cpdef increase_age(self):
        self.age += 1

cdef class PersonDataObject:
    cdef public str first_name
    cdef public str last_name
    cdef public int age

    def __cinit__(self, bytes first_name, bytes last_name, int age):
        self.first_name = first_name.decode('utf-8')
        self.last_name = last_name.decode('utf-8')
        self.age = age

    cpdef str get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    cpdef increase_age(self):
        self.age += 1

cdef void print_stats(double start, int objects_created):
    cdef double elapsed
    cdef double memory_usage
    elapsed = time.time() - start
    memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print("PID/TID: {}/{}, {} Objects in {:.3f} sec / {:.2f} MB".format(
        os.getpid(), threading.get_ident(), objects_created, 
        elapsed, memory_usage))

cpdef create_persons(str class_name="Person", int persons_num=1000000):
    cdef double start = time.time()
    cdef list persons = []
    cdef type person_class = globals()[class_name]
    cdef int i
    for i in range(1, persons_num + 1):
        person = person_class(b'John', b'Doe', 30)
        person.get_full_name()
        person.increase_age()
        persons.append(person)
        if i % 1000000 == 0:
            print_stats(start, i)


