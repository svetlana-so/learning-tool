import csv
import os
class Question:
    def __init__(self, question_text, answer, options = None):
        self.question_text = question_text
        self.answer = answer
        self.options = options

class Quiz:
    def __init__(self, file, capacity = 5): #default capacity is 5
        self.questions = []
        self.file = file
        self.capacity = capacity

    @property
    def capacity(self):
         return self._capacity

    @capacity.setter
    def capacity(self,value):
         if value < 5:
              raise ValueError('Add at least 5 questions')
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


    def read_from_csv(self):
        with open(self.file, 'r') as f:
             reader = csv.reader(f)
             header = next(reader) #skip the header row
             for row in reader:
                  question_text, answer, *options = row
                  options = options[:2] if options else None
                  question = Question(question_text, answer, options)
                  self.questions.append(question)

    def export_to_csv(self):
         with open(self.file, 'w') as f:
              writer = csv.writer(f)
              writer.writerow(['Question', 'Answer', 'Option1', 'Option2'])
              for question in self.questions:
                   writer.writerow([question.question_text, question.answer]+(question.options or [None]))

def main():
    file = 'questions.csv'
    quiz = Quiz(file)
    print('****Welcome to Interactive Learning Tool****')
    while True:
        print('1. Add question')
        print('2. Print the list')
        print('6. Finish')
        print('***************')
        choice = input('Enter your choice: ')
        print('***************')
        num_questions = len(quiz.questions)
        if choice == '1':
            while len(quiz.questions) < quiz.capacity:
                os.system('clear' if os.name == 'posix' else 'cls')
                print('Please provide at least 5 questions')
                print('***************')
                print('What type of question do you want to add?')
                print('1. Free form question')
                print('2. Quiz question')
                print('***************')
                question_choice = input('Enter your choice: ')
                if question_choice == '1':
                    quiz.add_free_form_question()
                elif question_choice == '2':
                    quiz.add_quiz_qiestion()
                print('The questions have been added to the list')
        elif choice == '2':
                quiz.read_from_csv()
                print('List of the exicting questions: ')
                for idx, question in enumerate(quiz.questions, start =1):
                     print(f'{idx}. {question.question_text}')
        elif choice == '6':
            print('The program is finished')
            break
        else:
            print('Invalid choice')



if __name__ == '__main__':
    main()     