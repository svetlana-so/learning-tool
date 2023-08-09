import csv
import os
class Question:
    def __init__(self, question_text, answer, options = None, enabled = True):
        self.question_text = question_text
        self.answer = answer
        self.options = options
        self.enabled = enabled

class Quiz:
    def __init__(self, file, capacity = 2): #default capacity is 5
        self.questions = []
        self.file = file
        self.capacity = capacity

    @property
    def capacity(self):
         return self._capacity

    @capacity.setter
    def capacity(self,value):
         if value < 2:
              raise ValueError('Add at least 2 questions')
         self._capacity = value

    def add_free_form_question(self):
            question_text = input('Enter your question: ')
            answer = input('Enter the answer: ')
            question=Question(question_text, answer)
            self.questions.append(question)

    def add_quiz_qiestion(self):
            question_text = input('Enter your question: ')
            answer = input('Enter the answer: ')
            option1 = input('Enter option 1: ')
            option2 = input('Enter option 2: ')
            options = [option1, option2]
            question=Question(question_text, answer, options)
            self.questions.append(question)

    def export_to_csv(self):
         with open(self.file, 'w') as f:
              writer = csv.writer(f)
              writer.writerow(['Question', 'Answer', 'Option1', 'Option2', 'Enabled'])
              for question in self.questions:
                   writer.writerow([question.question_text, question.answer]+(question.options or [None, None])+ [question.enabled])

    def read_from_csv(self):
        with open(self.file, 'r') as f:
             reader = csv.reader(f)
             header = next(reader) #skip the header row
             for idx, question in enumerate(self.questions, start =1):
                  print(f'{idx}. {question.question_text} {question.answer}')


    def save_status(self):
         with open('status.csv', 'w') as f:
              writer = csv.writer(f)
              writer.writerow(['Question', 'Answer', 'Option1', 'Option2', 'Status'])
              for question in self.questions:
                   writer.writerow([question.question_text, question.answer]+(question.options or [None, None])+[question.enabled])

    def update_question_statuses(self):
        while True:
            print('\nChoose the index of the question you want to disable/enable (or 0 to finish):')
            for idx, question in enumerate(self.questions, start=1):
                status = "Enabled" if question.enabled else "Disabled"
                print(f"{idx}. {question.question_text} - {status}")
            question_choice = int(input()) - 1
            if question_choice == -1:  # User wants to finish
                break
            if 0 <= question_choice < len(self.questions):
                self.questions[question_choice].enabled = not self.questions[question_choice].enabled
                print(f'Question "{self.questions[question_choice].question_text}" has been {"enabled" if self.questions[question_choice].enabled else "disabled"}.')
                self.save_status()
            else:
                print('Invalid question number.')
            another_choice = input('Do you want to disable/enable another question? (Y/n)').lower()
            if another_choice != 'y':
                break