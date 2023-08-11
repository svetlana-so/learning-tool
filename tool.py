from classes import Question, Quiz
import os
import emoji
from colorama import Fore, Style

def main():
    file = 'questions.csv'
    quiz = Quiz(file)
    quiz.load_questions()

    print(Fore.CYAN + Style.BRIGHT + emoji.emojize(":sparkles: Welcome to Interactive Learning Tool! :sparkles:") + Style.RESET_ALL)
    while True:
        print(Fore.MAGENTA + 'MAIN MENU' + Style.RESET_ALL)
        print('1. Add question')
        print('2. Disable/Enable Questions mode')
        print('3. Practice mode')
        print('4. Test mode')
        print('5. Statistics')
        print('6. Finish')
        print('***************')
        choice = input(Style.DIM +'Enter your choice: '+ Style.RESET_ALL)
        print('***************')
        os.system('clear' if os.name == 'posix' else 'cls')
        if choice == '1':
            print(Fore.CYAN + Style.BRIGHT + f'Current count of the question in provided file is: {len(quiz.questions)}' + Style.RESET_ALL)
            while True:
                print('***************')
                print('What type of question do you want to add?')
                print('1. Free form question')
                print('2. Quiz question')
                print('***************')
                question_choice = input('Enter your choice: ')
                os.system('clear' if os.name == 'posix' else 'cls')
                if question_choice == '1':
                    quiz.add_free_form_question()
                    os.system('clear' if os.name == 'posix' else 'cls')
                elif question_choice == '2':
                    quiz.add_quiz_qiestion()
                    os.system('clear' if os.name == 'posix' else 'cls')
                quiz.export_to_csv()
                print(Fore.MAGENTA + 'The question has been added to the list ✅ \n' + Style.RESET_ALL)
                add_another_question = input('Do you want to add another question? (Y/n)').lower()
                if add_another_question != 'y':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    break
        elif choice == '2':
            quiz.update_question_statuses()
        elif choice == '3':
            if len(quiz.questions) < 5:
                print('***************')
                print('Please provide at least 5 questions')
                print('***************')
                continue
            else:
                quiz.list_with_enabled_questions()
                quiz.start_practice_mode()
                os.system('clear' if os.name == 'posix' else 'cls')
        elif choice == '4':
            if len(quiz.questions) < 5:
                print('***************')
                print('Please provide at least 5 questions')
                print('***************')
                continue
            else:
                quiz.test_mode()
                os.system('clear' if os.name == 'posix' else 'cls')
        elif choice == '5':
            quiz.statistics()
        elif choice == '6':
            print('The program is finished')
            break
        else:
            print('Invalid choice')



if __name__ == '__main__':
    main()