from classes import Question, Quiz
import os

def main():
    file = 'questions.csv'
    quiz = Quiz(file)
    print('****Welcome to Interactive Learning Tool****')
    while True:
        print('1. Add question')
        print('2. Disable/Enable Questions mode')
        print('3. Practice mode')
        print('4. Test mode')
        print('5. Statistics')
        print('6. Finish')
        print('***************')
        choice = input('Enter your choice: ')
        print('***************')
        os.system('clear' if os.name == 'posix' else 'cls')
        if choice == '1':
            print(f'Please provide at least {quiz.capacity} questions')
            while len(quiz.questions) < quiz.capacity:
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
                quiz.export_to_csv()
                print('The questions have been added to the list\n')
                os.system('clear' if os.name == 'posix' else 'cls')
        elif choice == '2':
            print('This is the list of the existing questions: \n')
            quiz.read_from_csv()
            quiz.update_question_statuses()

        elif choice == '6':
            print('The program is finished')
            break
        else:
            print('Invalid choice')



if __name__ == '__main__':
    main()