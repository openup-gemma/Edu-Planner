# -*- coding: utf-8 -*-
"""gemma_eduplanner_total.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zkmXZ6JBupWsMuMpasuMh90tuZzPqziP
"""

# Using Gemma in Colab : https://hypro2.github.io/gemma-colab/
# https://webnautes.tistory.com/2275

"""# Google Drive Mount"""

from google.colab import drive
drive.mount('/content/drive')

"""# Dataset
### Source : https://devocean.sk.com/blog/techBoardDetail.do?ID=165703&boardType=techBlog
"""

# install needed sources
!pip install -q -U transformers==4.38.2
!pip install -q -U datasets==2.18.0
!pip install -q -U bitsandbytes==0.42.0
!pip install -q -U peft==0.9.0
!pip install -q -U trl==0.7.11
!pip install -q -U accelerate==0.27.2

# import needed sources
import torch
from datasets import Dataset, load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, TrainingArguments
from peft import LoraConfig, PeftModel
from trl import SFTTrainer

from huggingface_hub import notebook_login
notebook_login()

# load_dataset : about advices related to depression
dataset = load_dataset("ziq/depression_advice")
dataset # check dataset -> 'train', 'test'
dataset['train'][0] 
doc = dataset['train']['text'][0]

# load model : gemma-2b
BASE_MODEL = "google/gemma-2b-it" 
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map={"":0})
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, add_special_tokens=True)

# Chat Template : https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    { "role": "user",
     "content": "이번 모의고사 성적에서는 국어가 3등급이에요." }, # user's worries
]
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True) # chat template above

input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate( # .generate() method
    **input_ids,
    max_new_tokens=512,
    do_sample=True,
    top_p=0.95,
    temperature=0.7,
    repetition_penalty=1.1,
)

print(tokenizer.decode(outputs[0])) # answers are differnet everytime running this.