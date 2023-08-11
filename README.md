# learning-tool
 Interactive Learning Tool that allows users to create, practice, and test their knowledge using multiple-choice and freeform text questions.

Modes:

Adding questions.
Statistics viewing.
Disable/enable questions.
Practice mode.
Test mode.

Adding questions mode:
2 types of questions: 
- quiz questions 
- free-form text questions. 

The questions should be saved in a file so that once the program is closed and opened again, the questions remain.

The user should not be able to enter practice or test modes until at least 5 questions have been added.

Statistics viewing mode:
Print out all the questions currently in the system ( ID number; active or not; the question text; the number of times it was shown during practice or tests; the percentage of times it was answered correctly).


Disable/Enable Questions mode:
Users should be able to write the ID of the question they want to disable or enable. The question information (question text, answer) should be shown and the user should be asked to confirm whether they want to disable/enable it. Disabled questions should not appear in practice and test modes. The enabled/disabled status should be stored in a file, just like the questions (you should choose whether it is the same file or a different one).

Practice mode:
A mode in which questions are given non-stop so that the user can practice. However, the questions are chosen in such a way that the questions that are answered correctly become less likely to appear, while questions that are answered incorrectly become more likely to appear. Hint: you may want to look into weighted random choices. The probabilities should not be reset when the program restarts.

Test mode:
Users should first select the number of questions for the test which is not larger than the total number of questions added. The questions get chosen fully randomly and each question can only appear once at most in the test. At the end of the questions, the user is shown the score. The list of scores should be saved in a separate results.txt file – the date and time should be added next to the score as well.

