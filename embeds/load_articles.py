from langchain.text_splitter import MarkdownHeaderTextSplitter
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

loader = DirectoryLoader("../_output/articles", glob="./*.md", show_progress=True, loader_cls=UnstructuredMarkdownLoader)
data = loader.load()


embeddings = OpenAIEmbeddings(openai_api_key=keys.openai_key())

vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)

