from spacy import Language

from .char_normalizer import Char_Normalizer
from .date2string import Date2String
from .time2string import Time2String
from .num2string import Num2String
from .abbreviation import Abbreviation
from .punctuation_remover import Punc_remover
from .affix_norm import AffixNorm
from .spell_checker import SpellCheck
from .tokenizer import Tokenizer as parsivar_tokenizer
import spacy


# word and sentence tokenizer
# @Language.factory("disabletokenizer")
class WhitespaceTokenizer():
    def __init__(self,vocab):
        self.vacab = vocab

    def __call__(self, string):
        return string

# @Language.factory("CustomSentenceTokenizer")
# class CustomSentenceTokenizer():
#     def __init__(self):
#         self.tokenizer = parsivar_tokenizer()
#
#     def __call__(self, string):
#         return self.tokenizer.tokenize_sentences(string)

#


nlp = spacy.blank("fa")
# nlp.tokenizer = disabletokenizer()

# nlp.tokenizer_sentence = CustomSentenceTokenizer()


# -------------------------------------------
normalizer = Char_Normalizer()


@Language.component("char_normalizer")
def char_normalizer(doc):

    # print("char2str Process Done!")
    return normalizer.normalize(doc)


# -----------------------------------------------------------
date_2_string = Date2String()


@Language.component("date2str")
def date2str(doc):
    # print("date2str Process Done!")
    return date_2_string.normalize(doc)


# -----------------------------------------------------------
num_2_string = Num2String()


@Language.component("num2str")
def num2str(doc):
    # print("num2str Process Done!")

    return num_2_string.normalize(doc)


# -----------------------------------------------------------
time_2_string = Time2String()


@Language.component("time2str")
def time2str(doc):
    # print("time2str Process Done!")
    return time_2_string.normalize(doc)


# -----------------------------------------------------------
Abbreviation_2_word = Abbreviation()


@Language.component("abbreviation2word")
def Abbreviation2word(doc):
    # print("abb2str Process Done!")

    return Abbreviation_2_word.normalize(doc)


# -----------------------------------------------------------
parsivar_tokenizer = parsivar_tokenizer()


@Language.component("word_level_tokenizer")
def word_level_tokenizer(doc):
    # print("tokenize2str Process Done!")
    return parsivar_tokenizer.tokenize_words(doc)


# -----------------------------------------------------------
punc_remover = Punc_remover()


@Language.component("punctuation_remover")
def punctuation_remover(doc):
    # print("punc2str Process Done!")
    #
    return punc_remover.normalize(doc)


# -----------------------------------------------------------
affix = AffixNorm()


@Language.component("affix2norm")
def affix2norm(doc):
    # print("affix_norm Process Done!")
    return affix.normalize(doc)


# -----------------------------------------------------------
spell = SpellCheck()


@Language.component("spell_checker")
def spell_cheker(doc):
    # print("spell_cheker Process Done!")
    return spell.spell_corrector (doc)

@spacy.registry.tokenizers("whitespace_tokenizer")
def create_whitespace_tokenizer():
    def create_tokenizer(nlp):
        return WhitespaceTokenizer(nlp)

    return create_tokenizer
# -----------------------------------------------------------
nlp.tokenizer = WhitespaceTokenizer(nlp)
nlp.add_pipe("char_normalizer", first=True)
nlp.add_pipe("spell_checker",after="char_normalizer")
nlp.add_pipe("date2str", after="spell_checker")
nlp.add_pipe("time2str", after="date2str")
nlp.add_pipe("num2str", after="time2str")
nlp.add_pipe("abbreviation2word", after="num2str")
nlp.add_pipe("affix2norm", after="abbreviation2word")
nlp.add_pipe("punctuation_remover", after="abbreviation2word")
nlp.add_pipe("word_level_tokenizer")

#