import unittest
from classes import Question,Quiz



class TestQuizMethods(unittest.TestCase):

    def test_load_questions(self):
        quiz = Quiz('questions.csv')
        quiz.load_questions()
        assert len(quiz.questions) > 0, "No questions loaded from CSV"
        assert isinstance(quiz.questions[0], Question), "Loaded questions are not instances of Question class"

    def test_update_statistics(self):
        #create a mock question instance
        question = Question("Sample question", "Sample answer")
        #quiz instance and the mock questions to it
        quiz = Quiz('test_questions.csv')
        #simulate answering
        quiz.update_statistics(question, True)
        self.assertEqual(question.time_shown, 1)
        self.assertEqual(question.answered_correctly, 1)

    def test_question_initialization(self):
        question = Question("What is 2 + 2?", "4")
        self.assertEqual(question.question_text, "What is 2 + 2?")
        self.assertEqual(question.answer, "4")
        self.assertIsNone(question.options)
        self.assertTrue(question.enabled)
        self.assertEqual(question.weight, 1)
        self.assertEqual(question.time_shown, 0)
        self.assertEqual(question.answered_correctly, 0)

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()