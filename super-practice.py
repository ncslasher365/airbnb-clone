# PRACTICING INHERITANCE OF METHODS AND SUPER()
class Dog:
    def __init__(self):  # __init__ is calling when the object is created
        print("Barking on someone")

    def activity(self):
        print("I will go for walk, bro <3")


class Puppy(Dog):
    def __init__(self):
        print("Tiny boy, less gooo")
        super().__init__()


pug = Puppy()
