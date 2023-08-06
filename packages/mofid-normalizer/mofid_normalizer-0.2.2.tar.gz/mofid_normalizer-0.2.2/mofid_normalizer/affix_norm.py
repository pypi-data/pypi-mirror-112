from re import sub
import os
from .tokenizer import Tokenizer
from .data_helper import DataHelper
from .token_merger import ClassifierChunkParser
import re
from .stemmer import FindStems
class AffixNorm():

    def __init__(self,
                 half_space_char='\u200c',
                 statistical_space_correction=False,
                 train_file_path="resource/tokenizer/Bijan_khan_chunk.txt",
                 token_merger_path="resource/tokenizer/TokenMerger.pckl"):
        self.dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.dic1_path =  'mofid_normalizer/resource/normalizer/Dic1_new.txt'
        self.dic2_path = 'mofid_normalizer/resource/normalizer/Dic2_new.txt'
        self.dic3_path = 'mofid_normalizer/resource/normalizer/Dic3_new.txt'
        self.dic1 = self.load_dictionary(self.dic1_path)
        self.dic2 = self.load_dictionary(self.dic2_path)
        self.dic3 = self.load_dictionary(self.dic3_path)

        self.statistical_space_correction = statistical_space_correction


        self.data_helper = DataHelper()
        self.token_merger = ClassifierChunkParser()


        self.tokenizer = Tokenizer()
        self.space_normalizer = Spacenormalizer()

        if self.statistical_space_correction:
            self.token_merger_path = self.dir_path + token_merger_path
            self.train_file_path = train_file_path
            self.half_space_char = half_space_char

            if os.path.isfile(self.token_merger_path):
                self.token_merger_model = self.data_helper.load_var(self.token_merger_path)
            elif os.path.isfile(self.train_file_path):
                self.token_merger_model = self.token_merger.train_merger(self.train_file_path, test_split=0)
                self.data_helper.save_var(self.token_merger_path, self.token_merger_model)

    def load_dictionary(self, file_path):
        dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            g = f.readlines()
            for Wrds in g:
                wrd = Wrds.split(' ')
                dict[wrd[0].strip()] = sub('\n', '', wrd[1].strip())
        return dict

    def sub_alphabets(self, doc_string):

        a0 = "ء"
        b0 = "ئ"
        c0 = sub(a0, b0, doc_string)
        a1 = r"ٲ|ٱ|إ|ﺍ|أ"
        a11 = r"ﺁ|آ"
        b1 = r"ا"
        b11 = r"آ"
        c11 = sub(a11, b11, c0)
        c1 = sub(a1, b1, c11)
        a2 = r"ﺐ|ﺏ|ﺑ"
        b2 = r"ب"
        c2 = sub(a2, b2, c1)
        a3 = r"ﭖ|ﭗ|ﭙ|ﺒ|ﭘ"
        b3 = r"پ"
        c3 = sub(a3, b3, c2)
        a4 = r"ﭡ|ٺ|ٹ|ﭞ|ٿ|ټ|ﺕ|ﺗ|ﺖ|ﺘ"
        b4 = r"ت"
        c4 = sub(a4, b4, c3)
        a5 = r"ﺙ|ﺛ"
        b5 = r"ث"
        c5 = sub(a5, b5, c4)
        a6 = r"ﺝ|ڃ|ﺠ|ﺟ"
        b6 = r"ج"
        c6 = sub(a6, b6, c5)
        a7 = r"ڃ|ﭽ|ﭼ"
        b7 = r"چ"
        c7 = sub(a7, b7, c6)
        a8 = r"ﺢ|ﺤ|څ|ځ|ﺣ"
        b8 = r"ح"
        c8 = sub(a8, b8, c7)
        a9 = r"ﺥ|ﺦ|ﺨ|ﺧ"
        b9 = r"خ"
        c9 = sub(a9, b9, c8)
        a10 = r"ڏ|ډ|ﺪ|ﺩ"
        b10 = r"د"
        c10 = sub(a10, b10, c9)
        a11 = r"ﺫ|ﺬ|ﻧ"
        b11 = r"ذ"
        c11 = sub(a11, b11, c10)
        a12 = r"ڙ|ڗ|ڒ|ڑ|ڕ|ﺭ|ﺮ"
        b12 = r"ر"
        c12 = sub(a12, b12, c11)
        a13 = r"ﺰ|ﺯ"
        b13 = r"ز"
        c13 = sub(a13, b13, c12)
        a14 = r"ﮊ"
        b14 = r"ژ"
        c14 = sub(a14, b14, c13)
        a15 = r"ݭ|ݜ|ﺱ|ﺲ|ښ|ﺴ|ﺳ"
        b15 = r"س"
        c15 = sub(a15, b15, c14)
        a16 = r"ﺵ|ﺶ|ﺸ|ﺷ"
        b16 = r"ش"
        c16 = sub(a16, b16, c15)
        a17 = r"ﺺ|ﺼ|ﺻ"
        b17 = r"ص"
        c17 = sub(a17, b17, c16)
        a18 = r"ﺽ|ﺾ|ﺿ|ﻀ"
        b18 = r"ض"
        c18 = sub(a18, b18, c17)
        a19 = r"ﻁ|ﻂ|ﻃ|ﻄ"
        b19 = r"ط"
        c19 = sub(a19, b19, c18)
        a20 = r"ﻆ|ﻇ|ﻈ"
        b20 = r"ظ"
        c20 = sub(a20, b20, c19)
        a21 = r"ڠ|ﻉ|ﻊ|ﻋ"
        b21 = r"ع"
        c21 = sub(a21, b21, c20)
        a22 = r"ﻎ|ۼ|ﻍ|ﻐ|ﻏ"
        b22 = r"غ"
        c22 = sub(a22, b22, c21)
        a23 = r"ﻒ|ﻑ|ﻔ|ﻓ"
        b23 = r"ف"
        c23 = sub(a23, b23, c22)
        a24 = r"ﻕ|ڤ|ﻖ|ﻗ"
        b24 = r"ق"
        c24 = sub(a24, b24, c23)
        a25 = r"ڭ|ﻚ|ﮎ|ﻜ|ﮏ|ګ|ﻛ|ﮑ|ﮐ|ڪ|ك"
        b25 = r"ک"
        c25 = sub(a25, b25, c24)
        a26 = r"ﮚ|ﮒ|ﮓ|ﮕ|ﮔ"
        b26 = r"گ"
        c26 = sub(a26, b26, c25)
        a27 = r"ﻝ|ﻞ|ﻠ|ڵ"
        b27 = r"ل"
        c27 = sub(a27, b27, c26)
        a28 = r"ﻡ|ﻤ|ﻢ|ﻣ"
        b28 = r"م"
        c28 = sub(a28, b28, c27)
        a29 = r"ڼ|ﻦ|ﻥ|ﻨ"
        b29 = r"ن"
        c29 = sub(a29, b29, c28)
        a30 = r"ވ|ﯙ|ۈ|ۋ|ﺆ|ۊ|ۇ|ۏ|ۅ|ۉ|ﻭ|ﻮ|ؤ"
        b30 = r"و"
        c30 = sub(a30, b30, c29)
        a31 = r"ﺔ|ﻬ|ھ|ﻩ|ﻫ|ﻪ|ۀ|ە|ة|ہ"
        b31 = r"ه"
        c31 = sub(a31, b31, c30)
        a32 = r"ﭛ|ﻯ|ۍ|ﻰ|ﻱ|ﻲ|ں|ﻳ|ﻴ|ﯼ|ې|ﯽ|ﯾ|ﯿ|ێ|ے|ى|ي"
        b32 = r"ی"
        c32 = sub(a32, b32, c31)
        a33 = r'¬'
        b33 = r'‌'
        c33 = sub(a33, b33, c32)
        pa0 = r'•|·|●|·|・|∙|｡|ⴰ'
        pb0 = r'.'
        pc0 = sub(pa0, pb0, c33)
        pa1 = r',|٬|٫|‚|，'
        pb1 = r'،'
        pc1 = sub(pa1, pb1, pc0)
        pa2 = r'ʕ'
        pb2 = r'؟'
        pc2 = sub(pa2, pb2, pc1)
        na0 = r'۰|٠'
        nb0 = r'0'
        nc0 = sub(na0, nb0, pc2)
        na1 = r'۱|١'
        nb1 = r'1'
        nc1 = sub(na1, nb1, nc0)
        na2 = r'۲|٢'
        nb2 = r'2'
        nc2 = sub(na2, nb2, nc1)
        na3 = r'۳|٣'
        nb3 = r'3'
        nc3 = sub(na3, nb3, nc2)
        na4 = r'۴|٤'
        nb4 = r'4'
        nc4 = sub(na4, nb4, nc3)
        na5 = r'۵'
        nb5 = r'5'
        nc5 = sub(na5, nb5, nc4)
        na6 = r'۶|٦'
        nb6 = r'6'
        nc6 = sub(na6, nb6, nc5)
        na7 = r'۷|٧'
        nb7 = r'7'
        nc7 = sub(na7, nb7, nc6)
        na8 = r'۸|٨'
        nb8 = r'8'
        nc8 = sub(na8, nb8, nc7)
        na9 = r'۹|٩'
        nb9 = r'9'
        nc9 = sub(na9, nb9, nc8)
        ea1 = r'ـ|ِ|ُ|َ|ٍ|ٌ|ً|'
        eb1 = r''
        ec1 = sub(ea1, eb1, nc9)
        Sa1 = r'( )+'
        Sb1 = r' '
        Sc1 = sub(Sa1, Sb1, ec1)
        Sa2 = r'(\n)+'
        Sb2 = r'\n'
        Sc2 = sub(Sa2, Sb2, Sc1)

        return Sc2

    def space_correction(self, doc_string):
        a00 = r'^(بی|می|نمی)( )'
        b00 = r'\1‌'
        c00 = sub(a00, b00, doc_string)
        a0 = r'( )(می|نمی|بی)( )'
        b0 = r'\1\2‌'
        c0 = sub(a0, b0, c00)
        a1 = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
             r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )'
        b1 = r'‌\2\3'
        c1 = sub(a1, b1, c0)
        a2 = r'( )(شده|نشده)( )'
        b2 = r'‌\2‌'
        c2 = sub(a2, b2, c1)
        a3 = r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
             r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
             r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        b3 = r'‌\2\3'
        c3 = sub(a3, b3, c2)
        return c3

    def space_correction_plus1(self, doc_string):
        out_sentences = ''
        for wrd in doc_string.split(' '):
            try:
                out_sentences = out_sentences + ' ' + self.dic1[wrd]
            except KeyError:
                out_sentences = out_sentences + ' ' + wrd
        return out_sentences

    def space_correction_plus2(self, doc_string):
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 2:
            return doc_string
        cnt = 1
        for i in range(0, L - 1):
            w = wrds[i] + wrds[i + 1]
            try:
                out_sentences = out_sentences + ' ' + self.dic2[w]
                cnt = 0
            except KeyError:
                if cnt == 1:
                    out_sentences = out_sentences + ' ' + wrds[i]
                cnt = 1
        if cnt == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 1]
        return out_sentences

    def space_correction_plus3(self, doc_string):
        # Dict = {'گفتوگو': 'گفت‌وگو'}
        out_sentences = ''
        wrds = doc_string.split(' ')
        L = wrds.__len__()
        if L < 3:
            return doc_string
        cnt = 1
        cnt2 = 0
        for i in range(0, L - 2):
            w = wrds[i] + wrds[i + 1] + wrds[i + 2]
            try:
                out_sentences = out_sentences + ' ' + self.dic3[w]
                cnt = 0
                cnt2 = 2
            except KeyError:
                if cnt == 1 and cnt2 == 0:
                    out_sentences = out_sentences + ' ' + wrds[i]
                else:
                    cnt2 -= 1
                cnt = 1
        if cnt == 1 and cnt2 == 0:
            out_sentences = out_sentences + ' ' + wrds[i + 1] + ' ' + wrds[i + 2]
        elif cnt == 1 and cnt2 == 1:
            out_sentences = out_sentences + ' ' + wrds[i + 2]
        return out_sentences

    def normalize(self, doc_string):


        # normalized_string = self.data_helper.clean_text(normalized_string, new_line_elimination).strip()


        # if self.statistical_space_correction:
        #     token_list = normalized_string.strip().split()
        #     token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
        #     token_list = self.token_merger.merg_tokens(token_list, self.token_merger_model, self.half_space_char)
        #     normalized_string = " ".join(x for x in token_list)
        #     normalized_string = self.data_helper.clean_text(normalized_string, new_line_elimination)
        #
        # else:
        #     normalized_string = self.space_correction(self.space_correction_plus1(
        #         self.space_correction_plus2(self.space_correction_plus3(normalized_string)))).strip()
        #


        normalized_string = self.space_normalizer.convert_space(text_line=doc_string)

        return normalized_string


class Spacenormalizer():
    def __init__(self):
        self.stemmer = FindStems()

    def convert_space(self, text_line):
        text_line_list = text_line.split()

        text = ' '
        for word in text_line_list:
            result = self.stemmer.convert_to_stem(word)
            text += result + ' '
        text = re.sub("\u200c"," ",text)
        text = re.sub(' +', ' ', text)
        return "".join(text.rstrip().lstrip())
