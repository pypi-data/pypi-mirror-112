import sys
from sf import sflib


def main():
    print("hello from sf")
    student = sflib.Student("x", 12)
    print(student)
    assert(len(sys.argv) == 1)
