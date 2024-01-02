from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from key_helper import key_helper
import json

keys = key_helper()
client = MongoClient(keys.mongo_uri())
db_name = "battleBot0"
collection_name = "articles"
collection = client[db_name][collection_name]

loader = DirectoryLoader("../_process", glob="./*.txt", show_progress=True)
data = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=keys.openai_key())

# json.dump(embeddings, open("result.json","w", encoding="utf-8"))
vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)

