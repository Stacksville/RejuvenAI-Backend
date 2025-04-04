from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings

EMBEDDING_MODEL="text-embedding-3-large"

def get_vectordb()-> VectorStore: 
    """
        Creates a vectordb if the persist_directory does not exist. 
        Returns a VectorStore obj. 
        Action is idempotent. 
    """

    embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    db_name = "vdb_rejuvenai"

    vector_store = Chroma(
        collection_name="rejuvenai", 
        embedding_function=embeddings_model, 
        persist_directory=f"./{db_name}",
    )
    
    return vector_store



