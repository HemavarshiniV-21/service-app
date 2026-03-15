from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import os

def get_retriever():
    # Load documents
    loader = TextLoader("data/service_docs.txt")
    documents = loader.load()

    # Split documents
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Create vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Save vectorstore locally for persistence
    vectorstore.save_local("faiss_index")

    return vectorstore.as_retriever()

# Load if exists, else create
if os.path.exists("faiss_index"):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()
    except:
        retriever = None
else:
    retriever = None