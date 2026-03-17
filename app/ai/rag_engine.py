from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vector_db():

    loader = TextLoader("app/ai/knowledge/ml_knowledge.md")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="vector_db"
    )

    vectordb.persist()

    return vectordb

def retrieve_knowledge(query):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings
    )

    docs = vectordb.similarity_search(query, k=3)

    return [d.page_content for d in docs]