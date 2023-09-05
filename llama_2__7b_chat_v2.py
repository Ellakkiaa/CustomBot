# -*- coding: utf-8 -*-
"""llama-2 _7b_chat_v2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EuIAucIl74DZkx7uLjepEDfg1K3gbcfb
"""

import locale
def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding

!pip install transformers einops accelerate langchain bitsandbytes xformers sentence_transformers faiss-cpu

# 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

!huggingface-cli login

import torch
import transformers
from langchain import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model)

!pip install accelerate

pipeline = transformers.pipeline(
    "text-generation",
    model= model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=1000,
    do_sample=True,
    top_k=10,
    eos_token_id = tokenizer.eos_token_id
)

llm = HuggingFacePipeline(pipeline=pipeline,model_kwargs={'temperature':0})

"""question answering


"""

from langchain.chains.question_answering import load_qa_chain

from langchain.document_loaders import TextLoader
loader = TextLoader('/content/notes.txt')
docu = loader.load()

from langchain.document_loaders.onedrive_file import CHUNK_SIZE
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=5,chunk_overlap=0)
docs  = text_splitter.split_documents(docu)

from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings()

from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs,embeddings)

chain = load_qa_chain(llm,chain_type="stuff")

query = "what is the meeting name"
docs = db.similarity_search(query)
data = chain.run(input_documents = docs,question = query)
data

from langchain import PromptTemplate, LLMChain
from langchain.chains import SequentialChain

template = """
             explain about the {data} in 3 lines

           """

prompt = PromptTemplate(template = template,input_variables=["data"])

llm_chain = LLMChain(prompt=prompt,llm=llm)

print(llm_chain.run(data))

