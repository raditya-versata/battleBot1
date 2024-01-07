import sys

from langchain.document_loaders import UnstructuredMarkdownLoader
from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from key_helper import key_helper

keys = key_helper()
client = MongoClient(keys.mongo_uri())
db_name = "battleBot0"
collection_name = "articles_md"
collection = client[db_name][collection_name]

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
   keys.mongo_uri(),
   db_name + "." + collection_name,
   OpenAIEmbeddings(openai_api_key=keys.openai_key(),disallowed_special=()),
   index_name="article_md_idx"
)

qa_retriever = vector_search.as_retriever(
   search_type="similarity",
   search_kwargs={
       "k": 200,
       "post_filter_pipeline": [{"$limit": 25}]
   }
)
from langchain.prompts import PromptTemplate
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
fbi

{context}


Question: {question}
"""
PROMPT = PromptTemplate(
   template=prompt_template, input_variables=["context", "question"]
)
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=keys.openai_key()),chain_type="stuff", retriever=qa_retriever, return_source_documents=True,
                                 chain_type_kwargs={"prompt": PROMPT})


docs = qa({"query": "The GROWMARK hosted DNN sites are having a critical issue where the Text/HTML sections on all of our websites are displaying errors suddenly this morning. Ex. https://www.example.com/. Can we get immediate assistance with this?"})


print(docs["result"])
print(docs['source_documents'])