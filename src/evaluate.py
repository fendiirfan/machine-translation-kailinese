import os
import shutil
from copy import deepcopy
import random
import numpy as np
import pandas as pd
import torch
from torch import optim
from torch.optim.lr_scheduler import StepLR
from tqdm import tqdm
from transformers import AdamW, T5Tokenizer
from nltk.tokenize import TweetTokenizer
from modules.tokenization_indonlg import IndoNLGTokenizer
from modules.tokenization_mbart52 import MBart52Tokenizer




###
# modelling functions
###
def get_lr(args, optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']
    
# Evaluate function for validation and test
def evaluate(model, data_loader, forward_fn, model_type, tokenizer, beam_size=1, max_seq_len=512, is_test=False, device='cpu', length_penalty=1.0):
    model.eval()
    torch.set_grad_enabled(False)
    list_hyp, list_label = [], []

    pbar = tqdm(iter(data_loader), leave=True, total=len(data_loader))
    for i, batch_data in enumerate(pbar):
        batch_seq = batch_data[-1]
        batch_hyp, batch_label = forward_fn(model, batch_data, model_type=model_type, tokenizer=tokenizer, device=device, is_inference=is_test, 
                                                      is_test=is_test, skip_special_tokens=True, beam_size=beam_size, max_seq_len=max_seq_len, length_penalty=length_penalty)
        
        list_hyp += batch_hyp
        list_label += batch_label
    
    
    
    return list_hyp, list_label
