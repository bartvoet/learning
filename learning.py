import random
import csv
import sys
from os import system, name 

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
        return self.left + " => " + ', '.join([str(elem) for elem in self.right])

class ConsoleQuestionInterface:

    def clearConsole(self): 
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    def printQuestion(self,question):
        print(question + ": ")

    def get(self):
        return input("> ")

    def ask(self,question):
        self.clearConsole()
        return print(question + ": ") 

    def printRemaining(self,remaining,total,errors):
        self.clearConsole()
        print("({} of {} remaining)".format(remaining,total))
        if len(errors) > 0:
            print("Errors:")
        for error in errors:
            print("=> ",error.hint())
        input("Type enter to continue")

    def printError(self,error):
        print("Wrong: {}".format(error.hint()))
        input("Enter to continue")

    def printEnd(self):
        print("Done!!!")

class QuestionState:
    def __init__(self,questions,interface):
        self.initQuestions = questions
        self.questions = questions.copy()
        self.errors = []
        self.counter = 0
        self.interface = interface

    def questionsRemaining(self):
        return len(self.questions)

    def checkCounter(self):
        interrupt_at = 5
        self.counter = self.counter + 1
        if self.counter % interrupt_at == 0:
            self.interface.printRemaining(self.questionsRemaining(),len(self.initQuestions),self.errors)

    def removeQuestion(self,item):
        self.questions.remove(item)
        if item in self.errors:
            self.errors.remove(item)

    def addError(self,item):
        if item not in self.errors:
            self.errors.append(item)

    def nextQuestion(self):
        self.checkCounter()
                
        random_pic = random.randint(0,len(self.questions)-1)
        item = self.questions[random_pic]
        
        if item.checkAnswer(self.interface):
            self.removeQuestion(item)
        else:
            self.addError(item)
            self.interface.printError(item)
      
    def run(self):
        while self.questionsRemaining() > 0:
            self.nextQuestion()
        self.interface.printEnd()

fileQuestions = []

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        question = row[0]
        answers = list(filter(None,row[1:]))
        fileQuestions.append(Question(question,answers))
    interface = QuestionState(fileQuestions,ConsoleQuestionInterface())

interface.run()