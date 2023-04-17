import pandas as pd
import pickle
# import torch
import json
from utils.data_utils import MachineTranslationDataset, GenerationDataLoader
from utils.train_eval import evaluate
import uuid
from utils.metrics import generation_metrics_fn
from utils.forward_fn import forward_generation
from transformers import AutoModelForSeq2SeqLM
import os




class Predict:
    def __init__(self, text_input):
        self.text_input = text_input
        self.kamus_alay1_dir = 'resource/colloquial-indonesian-lexicon1.csv'
        self.kamus_alay2_dir = 'resource/colloquial-indonesian-lexicon2.csv'
        self.model_dir = 'model_result/best_model_0.th'
        self.tokenizer_dir = 'model_result/tokenizer.pickle'
        self.input_id = f'{uuid.uuid4()}'
        self.input_dir = f'.user_input/{self.input_id}.json'
        self.model_type = 'indo-bart'
        self.max_seq_len = 512

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
        # model = torch.load(self.model_dir, map_location=torch.device('cpu'))
        # model = AutoModelForSeq2SeqLM.from_pretrained('/home/fendi_amorokhman/machine-trainslation-kaili/model_result')
        with open('/home/fendi_amorokhman/machine-trainslation-kaili/model_result/model.pickle', 'rb') as handle:
            model = pickle.load(handle)
        return model

    def load_tokenizer(self):
        with open(self.tokenizer_dir, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer
    import json
    def text_to_json(self):
        
        data = [{'id': self.input_id, 'text': self.input_id, 'label': self.text_input}]
        json_data = json.dumps(data)
        
        with open(self.input_dir, 'w') as f:
            f.write(json_data)
    def adjust_input_text(self):
        self.tokenizer = self.load_tokenizer()
        lower = True

        no_special_token = False
        swap_source_target = True
        
        separator_id = 4
        speaker_1_id = 5
        speaker_2_id = 6

        test_batch_size = 8

        source_lang = "[indonesian]"
        target_lang = "[sundanese]"

        src_lid = self.tokenizer.special_tokens_to_ids[source_lang]
        tgt_lid = self.tokenizer.special_tokens_to_ids[target_lang]
        self.text_to_json()
        test_dataset = MachineTranslationDataset(self.input_dir, self.tokenizer, lowercase=lower, no_special_token=no_special_token, 
                                            speaker_1_id=speaker_1_id, speaker_2_id=speaker_2_id, separator_id=separator_id,
                                            max_token_length=self.max_seq_len, swap_source_target=swap_source_target)
        test_loader = GenerationDataLoader(dataset=test_dataset, model_type=self.model_type, tokenizer=self.tokenizer, max_seq_len=self.max_seq_len, 
                                   batch_size=test_batch_size, src_lid_token_id=src_lid, tgt_lid_token_id=tgt_lid, num_workers=8, shuffle=False)
        return test_loader
    def translate(self):
        self.text_input = self.preprocessing()
        model = self.load_model()
        test_loader = self.adjust_input_text()
        test_loss, test_metrics, test_hyp, test_label = evaluate(model, data_loader=test_loader, forward_fn=forward_generation, 
                                                         metrics_fn=generation_metrics_fn, model_type=self.model_type, 
                                                         tokenizer=self.tokenizer, beam_size=5, 
                                                         max_seq_len=self.max_seq_len, is_test=True, 
                                                         device='cpu')
        os.remove(self.input_dir)
        return test_hyp[0]
        

