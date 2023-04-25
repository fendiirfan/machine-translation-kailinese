import pandas as pd
import pickle
import json
from src.data_utils import MachineTranslationDataset, GenerationDataLoader
from src.evaluate import evaluate
import uuid
from src.forward_fn import forward_generation
from transformers import AutoModelForSeq2SeqLM
import streamlit as st    


class Predict:
    def __init__(self, text_input, lang_src):
        self.base_dir = st.secrets["base_dir"]
        self.text_input = text_input
        self.kamus_alay1_dir = self.base_dir+'input/colloquial-indonesian-lexicon1.csv'
        self.kamus_alay2_dir = self.base_dir+'input/colloquial-indonesian-lexicon2.csv'
        
        self.input_id = f'{uuid.uuid4()}'
        self.model_type = 'indo-bart'
        self.max_seq_len = 512
        self.min_count_word = 3
        self.max_count_word = 40

        if lang_src=='Indonesian':
            self.swap_source_target = True
            self.model_dir = self.base_dir+'model/indo_ke_kaili'
            self.tokenizer_dir = self.base_dir+'model/indo_ke_kaili/tokenizer.pickle'
        elif lang_src=='Kailinese':
            self.swap_source_target = False
            self.model_dir = self.base_dir+'model/kaili_ke_indo'
            self.tokenizer_dir = self.base_dir+'model/kaili_ke_indo/tokenizer.pickle'

    def preprocessing(self):
        kamus_alay1 = pd.read_csv(self.kamus_alay1_dir)
        kamus_alay2 = pd.read_csv(self.kamus_alay2_dir)

        self.text_input = self.text_input.replace("\n", ". ").replace("-", " ")
        splited_text = self.text_input.split(' ')
        word_temp = []
        # Iterate over each word in the text
        for word in splited_text:
            # Try to find the word in the second mapping
            try:
                index = kamus_alay2[kamus_alay2['slang'] == word].index[0]
                word_kamus_alay2 = kamus_alay2.loc[index, 'formal']
                # Try to find the formal word in the first mapping
                try:
                    index_kamus_alay1 = kamus_alay1[kamus_alay1['kataAlay'] == word_kamus_alay2].index[0]
                    word_temp.append(kamus_alay1.loc[index_kamus_alay1, 'kataBaik'])
                except IndexError:
                    # If the formal word is not found in the first mapping, use the original formal word from the second mapping
                    word_temp.append(word_kamus_alay2)
            # If the word is not found in the second mapping, try to find it in the first mapping
            except IndexError:
                try:
                    index = kamus_alay1[kamus_alay1['kataAlay'] == word].index[0]
                    word_temp.append(kamus_alay1.loc[index, 'kataBaik'])
                except IndexError:
                    # If the word is not found in either mapping, use the original word
                    word_temp.append(word)

        cleaned_text = ' '.join(word_temp)
        return cleaned_text
    
    
    def load_model(self):
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_dir)
        return model

    def load_tokenizer(self):
        with open(self.tokenizer_dir, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer
    def adjust_input_text(self):
        self.tokenizer = self.load_tokenizer()
        lower = True

        no_special_token = False
        
        separator_id = 4
        speaker_1_id = 5
        speaker_2_id = 6

        test_batch_size = 1

        source_lang = "[indonesian]"
        target_lang = "[sundanese]"

        src_lid = self.tokenizer.special_tokens_to_ids[source_lang]
        tgt_lid = self.tokenizer.special_tokens_to_ids[target_lang]
        self.input_data = [{
                'id' : self.input_id,
                'text': self.text_input,
                'label': self.text_input
                }]
        
        test_dataset = MachineTranslationDataset(self.input_data, self.tokenizer, lowercase=lower, no_special_token=no_special_token, 
                                            speaker_1_id=speaker_1_id, speaker_2_id=speaker_2_id, separator_id=separator_id,
                                            max_token_length=self.max_seq_len, swap_source_target=self.swap_source_target)
        test_loader = GenerationDataLoader(dataset=test_dataset, model_type=self.model_type, tokenizer=self.tokenizer, max_seq_len=self.max_seq_len, 
                                   batch_size=test_batch_size, src_lid_token_id=src_lid, tgt_lid_token_id=tgt_lid, num_workers=0, shuffle=False)

        return test_loader
    def translate(self):
        len_user_input = len(self.text_input.split(' '))

        if len_user_input<self.min_count_word:
            return f'⚠️ Limit the word count to {self.min_count_word} minimum ⚠️'
        elif len_user_input>self.max_count_word:
            return f'⚠️ Limit the word count to {self.max_count_word} maximum ⚠️'
        else:
            self.text_input = self.preprocessing()
            test_loader = self.adjust_input_text()
            model = self.load_model()
            test_hyp, test_label = evaluate(model, data_loader=test_loader, forward_fn=forward_generation, 
                                                            model_type=self.model_type, 
                                                            tokenizer=self.tokenizer, beam_size=5, 
                                                            max_seq_len=self.max_seq_len, is_test=True, 
                                                            device='cpu')
            
            
            return test_hyp[0]        

