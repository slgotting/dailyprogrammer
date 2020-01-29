import logging

logging.basicConfig(filename='easy-py.log', level=logging.INFO, format='%(asctime)s %(message)s')


class Person:
    def __init__(self, name, age, username):
        self.name = name
        self.age = age
        self.username = username

    def __str__(self):
        return f"User {self.username}'s name is {self.name} and they are {self.age} years old"


def create_person():
    questions = ['name', 'age', 'username']
    answers = []
    for q in questions:
        answers.append(input(f"What is your {q}? "))
    
    new_person = Person(*answers)
    print('your name is {}, you are {} years old, and your username is {}'.format(*answers))
    logging.info(new_person)

create_person()

