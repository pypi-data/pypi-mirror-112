
import re


class Punc_remover():

    def __init__(self):
        self.punctuation_normalizer = Punctuation()

    def normalize(self, doc_string):
        normalized_string = self.punctuation_normalizer.convert_punctuation(text_line=doc_string)

        return normalized_string


class Punctuation():
    def __init__(self):
        self.punctuation_list = []

    def convert_punctuation(self, text_line):

        input_data = re.sub(r'[^\w\s]', '', text_line)

        return ''.join(input_data)


