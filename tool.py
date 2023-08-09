import csv
class QuestionsList:
    def __init__(self, file_name):
        self.questions = []
        self.file_name = file_name
    @property
    def file_name(self):
        return self._file_name
    @file_name.setter
    def file_name(self, new_file_name):
        self._file_name = new_file_name      
    