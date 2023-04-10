import pandas as pd
import pickle
import torch

class Translator:
    def __init__(self, text_input):
        self.text_input = text_input
        self.kamus_alay1_dir = 'resource/colloquial-indonesian-lexicon1.csv'
        self.kamus_alay2_dir = 'resource/colloquial-indonesian-lexicon2.csv'
        self.model_dir = 'model_result/best_model_0.th'
        self.tokenizer_dir = 'model_result/tokenizer.pickle'

    def preprocessing(self):
        kamus_alay1 = pd.read_csv(self.kamus_alay1_dir)
        kamus_alay2 = pd.read_csv(self.kamus_alay2_dir)

        splited_text = self.text_input.split(' ')
        word_temp = []

        for word in splited_text:
            try:
                index = kamus_alay2[kamus_alay2['slang'] == word].index[0]
                word_kamus_alay2 = kamus_alay2.loc[index, 'formal']
                try:
                    index_kamus_alay1 = kamus_alay1[kamus_alay1['kataAlay'] == word_kamus_alay2].index[0]
                    word_temp.append(kamus_alay1.loc[index_kamus_alay1, 'kataBaik'])
                except IndexError:
                    word_temp.append(word_kamus_alay2)
            except IndexError:
                try:
                    index = kamus_alay1[kamus_alay1['kataAlay'] == word].index[0]
                    word_temp.append(kamus_alay1.loc[index, 'kataBaik'])
                except IndexError:
                    word_temp.append(word)

        cleaned_text = ' '.join(word_temp)
        return cleaned_text

    def load_model(self):
        model = torch.load(self.model_dir, map_location=torch.device('cpu'))
        return model

    def load_tokenizer(self):
        with open(self.tokenizer_dir, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer

    def translate(self):
        cleaned_text = self.preprocessing()
        model = self.load_model()
        tokenizer = self.load_tokenizer()

