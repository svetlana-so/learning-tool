import csv
import os
import random
import numpy as np
from datetime import datetime
from colorama import Fore, Style
import emoji

class Question:
    def __init__(self, question_text, answer, options = None, enabled = True, weight = 1):
        self.question_text = question_text
        self.answer = answer
        self.options = options
        self.enabled = enabled
        self.weight = weight
        self.time_shown = 0
        self.answered_correctly = 0

class Quiz:
    def __init__(self, file):
        self.file = file
        self.questions = []
        self.enabled_questions = []

    def update_statistics(self, question, is_correct):
        question.time_shown += 1
        if is_correct:
            question.answered_correctly += 1


#check if this file exists and load questions to self.questions with the instances of the Question class
    def load_questions(self):
         if os.path.exists(self.file) and os.path.getsize(self.file)>0:
              with open(self.file, 'r') as f:
                reader = csv.reader(f) #creaste a csv reader object
                header = next(reader) #reads the first row of csv
                for row in reader:
                    question_text, answer, option1, option2, enabled , weight = row
                    weight = float(weight) if weight else 1.0
                    self.questions.append(Question(question_text, answer, [option1, option2], enabled, weight))

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
    def is_quiz_qiestion(self, question):
        return question.options is not None and len(question.options)>0

    #add the new questions to file
    def export_to_csv(self):
         with open(self.file, 'w') as f:
              writer = csv.writer(f)
              writer.writerow(['Question', 'Answer', 'Option1', 'Option2', 'Status', 'Weight'])
              for question in self.questions:
                   writer.writerow([question.question_text, question.answer]+(question.options or [None, None])+ [question.enabled, question.weight])


#this rewrite the file when we uppdate status of the question
    def save_status(self):
        with open('status.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Question', 'Answer', 'Option1', 'Option2', 'Status', 'Weight'])
            for question in self.questions:
                writer.writerow([question.question_text, question.answer] + (question.options or [None, None]) + [question.enabled, question.weight])

    def update_question_statuses(self):
        while True:
            print(Fore.MAGENTA +'\nChoose the index of the question you want to disable/enable (or 0 to finish):'+ Style.RESET_ALL)
            for idx, question in enumerate(self.questions, start=1):
                status = "Enabled" if question.enabled else "Disabled"
                print(f"{idx}. {question.question_text} - " + Fore.CYAN + Style.BRIGHT+ f"{status}" + Style.RESET_ALL)
            question_choice = int(input()) - 1
            os.system('clear' if os.name == 'posix' else 'cls')
            if question_choice == -1:  # User wants to finish
                break
            if 0 <= question_choice < len(self.questions):
                self.questions[question_choice].enabled = not self.questions[question_choice].enabled
                print(f'Question "{self.questions[question_choice].question_text}" has been {"enabled" if self.questions[question_choice].enabled else "disabled"}.')
            else:
                print('Invalid question number.')
            another_choice = input(Fore.MAGENTA +'Do you want to disable/enable another question? (Y/n)' + Style.RESET_ALL).lower()
            if another_choice != 'y':
                break
        self.save_status()
        os.system('clear' if os.name == 'posix' else 'cls')

#create a list of the question which are enabled that we have chosen for our practice mode
    def list_with_enabled_questions(self):
        with open('status.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                question_text, answer, option1, option2, status, weight = row
                if status.lower() == 'true':
                    self.enabled_questions.append(Question(question_text, answer, [option1, option2], status, weight))


    def start_practice_mode(self):
        self.list_with_enabled_questions()  # Load enabled questions from the status file
        #check if there are enabled questions available
        if not self.enabled_questions:
            print("No enabled questions available for practice.")
            return
        quit_command = 'quit'
        print(Fore.MAGENTA + f'To quit the mode please enter "{quit_command}" as your answer.\n' + Style.RESET_ALL)

        # Create an array of question weights which determine the likelihood of selectiong a specific question
        question_weights = np.array([float(question.weight) for question in self.enabled_questions])

        while True:
            #create a probability of distribution by deviding each weight by the sum of all weights
            test_questions_index = np.random.choice(len(self.enabled_questions), p=question_weights / question_weights.sum())
            #get a selected question
            test_questions = self.enabled_questions[test_questions_index]

            print(f'Question: {test_questions.question_text}')
            if test_questions.options and test_questions.options[0] and test_questions.options[1]:
                options = test_questions.options + [test_questions.answer]
                random.shuffle(options)
                for option_num, option in enumerate(options, start=1):
                    print(f"{chr(96 + option_num)}. {option}")
            user_answer = input("Your answer: ")
            if user_answer.lower() == test_questions.answer.lower():
                print("🌟" + Fore.GREEN + "CORRECT!" + Style.RESET_ALL + "🌟")
                question_weights[test_questions_index] *= 0.8  # Decrease weight for correct answers
                self.update_statistics(test_questions, True)
            else:
                print(Fore.RED + "INCORRECT!" + Style.RESET_ALL)
                question_weights[test_questions_index] *= 1.2  # Increase weight for incorrect answers
                self.update_statistics(test_questions, False)
            #update thr question's weight with the new one
            test_questions.weight = question_weights[test_questions_index]  # Update question's weight
            #update the weight colomn in csv file
            formated_w = f'{test_questions.weight:.2f}'

            # Update the weight column in the status CSV
            with open('status.csv', 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = list(reader)
            for row in rows:
                if row[0] == test_questions.question_text:
                    row[-1] = formated_w

            with open('status.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)

            
            if user_answer.lower() == quit_command:
                break


    def test_mode(self):
        self.list_with_enabled_questions()
        print(Fore.MAGENTA + '✨Welcome to the test mode✨' + Style.RESET_ALL)
        num_questions = int(input(f'Enter the number of questions for the test (1 - {len(self.enabled_questions)}): '))
        if num_questions < 1 or num_questions > len(self.enabled_questions):
            print('Invalid number of questions')
            return
        #select a random subset of enabled questions for the test from enabled questions list
        test_questions = random.sample(self.enabled_questions, num_questions)
        score = 0

        for num, question in enumerate(test_questions, start=1):
            print(f"Question {num}: {question.question_text}")

            if question.options and question.options[0] and question.options[1]:
                options = question.options + [question.answer]
                random.shuffle(options)
                for option_num, option in enumerate(options, start=1):
                    print(f"{chr(96 + option_num)}. {option}")
            user_answer = input("Your answer: ").lower()
            if user_answer == question.answer.lower():
                print("🌟" + Fore.GREEN + "CORRECT!" + Style.RESET_ALL + "🌟")
                score += 1

            else:
                print(Fore.RED + "INCORRECT!" + Style.RESET_ALL)

        print(f"You scored {score}/{num_questions} in the test mode.")

        # Save score in results.txt
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('results.txt', 'a') as f:
            f.write(f"Test is taken on {timestamp}: Score = {score}/{num_questions}\n")

        print(f"Test completed. Your score: {score}/{num_questions}")

    def statistics(self):
        with open('status.csv', 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            question_data = list(reader)

        print(Fore.MAGENTA +"Question Statistics:" + Style.RESET_ALL)
        print(f"{:<5} | {:<10} | {:<80} | {:<15} | {:<15} | {:<15}".format("ID", "Active", "Question Text", "Practice Count", "Times Correct", "Percentage"))
        print("-" * 150)

        for id, row in enumerate(question_data, start=1):
            question_text, _, _, _, status, weight = row
            practice_count_str = row[-3]
            try:
                practice_count = int(practice_count_str)
            except ValueError:
                practice_count = 0

            times_correct_str = row[-2]
            try:
                times_correct = int(times_correct_str)
            except ValueError:
                times_correct = 0

            if practice_count > 0:
                percentage_correct = (times_correct / practice_count) * 100
            else:
                percentage_correct = 0.0

            active = "Active" if status.lower() == 'true' else "Inactive"
            appearance_count = 0  # Default value in case the question is not found
            for question in self.questions:
                if question.question_text == question_text:
                    appearance_count = question.time_shown
                    break

            print(f"{:<5} | {:<10} | {:<80} | {:<15} | {:<15} | {:<15.2f}%".format(id, active, question_text, appearance_count, times_correct, percentage_correct))
        input(Fore.CYAN + '\nPress enter to go back to the main menu' + Style.RESET_ALL)
        os.system('clear' if os.name == 'posix' else 'cls')


#https://github.com/svetlana-so/card-game-war



