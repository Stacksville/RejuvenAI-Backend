from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import SQLRecordManager, index
from langchain_community.document_loaders import (
    PyMuPDFLoader,
)
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings


def get_vectordb(mock: bool = False)-> VectorStore: 
    """
        Creates a vectordb if the persist_directory does not exist. 
        Returns a VectorStore obj. 
        Action is idempotent. 
    """

    embeddings_model = OpenAIEmbeddings()

    db_name = "cdb_rejuvenai"

    if mock: 
        db_name = "mock_" + db_name

    vector_store = Chroma(
        collection_name="rejuvenai", 
        embedding_function=embeddings_model, 
        persist_directory=f"./{db_name}",
    )
    
    return vector_store

def load_knowledge_base(): 
    pass

def mock_knowledge_base(datasource_path: str) -> None: 
    """
        Adds PDF documents present in the datasource_path to the vectodb 
        The action is idempotentA
    """

    vectordb = get_vectordb(mock=True)

    pdf_directory = Path(datasource_path)
    docs = []  ##type: List[Document]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for pdf_path in pdf_directory.glob("*.pdf"):
        loader = PyMuPDFLoader(str(pdf_path))
        documents = loader.load()
        docs += text_splitter.split_documents(documents)

    if not docs: 
        print("No mock documents found in the specified directory. Exiting...")
        raise SystemExit
    #doc_search = Chroma.from_documents(docs, embeddings_model) 

    vectordb.add_documents(documents=docs)


    namespace = "chromadb/rejuvenai"
    record_manager = SQLRecordManager(
        namespace, db_url="sqlite:///record_manager_cache.sql"
    )
    record_manager.create_schema()

    index_result = index(
        docs,
        record_manager,
        vectordb,
        cleanup="incremental",
        source_id_key="source",
    )

    print(f"Indexing stats: {index_result}")



    



