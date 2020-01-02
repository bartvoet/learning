import random
import csv
import sys
from os import system, name 

def clear_console(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

class Question:
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def question(self):
        return self.left

    def checkAnswer(self,interface):
        answers = self.right.copy()
        interface.ask(self.left)
        while len(answers) != 0:
            answer = interface.get()
            if answer in answers:
                answers.remove(answer)
            else:
                return False
        return True

    def hint(self):
        return self.right[0]

class QuestionInterface:
    def __init__(self,questions):
        self.questions = questions.copy()

    def ask(self,question):
        return print(question + ": ") 

    def get(self):
        return input("> ")

    def questionsRemaining(self):
        return len(self.questions) == 0

    def run(self):
        while True:
            if(self.questionsRemaining()):
                return
            clear_console()

            random_pic = random.randint(0,len(self.questions)-1)
            item = self.questions[random_pic]
            
            if item.checkAnswer(interface):
                self.questions.remove(item)
            else:
                print("Wrong should be {}".format(item.hint()))
                input("Enter to continue")

fileQuestions = []


with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        question = row[0]
        answers = list(filter(None,row[1:]))
        fileQuestions.append(Question(question,answers))
    interface = QuestionInterface(fileQuestions)

interface.run()