from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader
from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from key_helper import key_helper

keys = key_helper()
client = MongoClient(keys.mongo_uri())
db_name = "battleBot0"
collection_name = "articles_md_split"
collection = client[db_name][collection_name]

loader = DirectoryLoader("../_output/articles", glob="./*.md", show_progress=True,
                         loader_cls=UnstructuredMarkdownLoader)
data = loader.load()

# Define the Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

# Create a split of the document using the text splitter
splits = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(openai_api_key=keys.openai_key())

vectorStore = MongoDBAtlasVectorSearch.from_documents(splits, embeddings, collection=collection)
