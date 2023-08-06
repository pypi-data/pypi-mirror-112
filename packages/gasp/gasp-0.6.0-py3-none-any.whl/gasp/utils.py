import string
import random


def read_number(prompt="Please enter a number: "):
    if prompt != "" and prompt[-1] not in string.whitespace:
        prompt += " "

    while True:
        result = input(prompt)
        try:
            return int(result)
        except ValueError:
            try:
                return float(result)
            except ValueError:
                print("But that wasn't a number!\n")


def read_yesorno(prompt="Yes or no? "):
    if prompt != "" and prompt[-1] not in string.whitespace:
        prompt += " "

    while True:
        result = input(prompt)
        if result.lower() in ["y", "yes"]:
            return True
        elif result.lower() in ["n", "no"]:
            return False
        print("Please answer yes or no.\n")


def random_between(a, b):
    return random.randint(a, b)


def random_choice(list):
    return random.choice(list)


def add_vectors(v1, v2):
    x = v1[0] + v2[0]
    y = v1[1] + v2[1]
    return x, y


def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
