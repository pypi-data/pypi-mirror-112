import re


class Abbreviation():

    def __init__(self):
        self.abbreviation_normalizer = AbbreviationNormalizer()

    def normalize(self, doc_string):
        normalized_string = self.abbreviation_normalizer.find_abbreviation_part(text_line=doc_string)

        return normalized_string


class AbbreviationNormalizer():
    def __init__(self):
        self.abbreviation_rules = r'( ه ق )|( ه ش )|( ه.ق )|( ه.ش )|( ع )|( ره )|(\(ه ش\))|(\(ه ق\))|(\(ه.ش\))|(\(ه.ق\))|(\(ره\))|(\(ع\))|( ه ق )|( ه ش )|( ه.ق. )|( ه.ش. )|( ره )|(\(ه ش\))|(\(ه ق\))|(\(.ه.ش\))|(\(ه.ق.\))|(\(ره\))|(\(ع\))'
        self.abbreviation_dictionary = {
            'هق': ' هجری قمری ',
            'هش': ' هجری شمسی ',
            'ره': ' رحمه الله ',
            'ع': ' علیه السلام '
        }

    def find_abbreviation_part(self, text_line):
        content_new = re.sub(self.abbreviation_rules, lambda x: self.abbreviation_converter(x.group()), " "+text_line+" ")

        return content_new.lstrip().strip()

    def abbreviation_converter(self, input_data):
        try:
            return self.abbreviation_dictionary[re.sub('\W+', "", input_data)]
        except:
            return input_data



