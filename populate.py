# prepopulates vector embeddings into the vectordb

from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import IndexingResult, SQLRecordManager, index
from langchain_community.document_loaders import (
    PyMuPDFLoader,
)
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from vectordb import get_vectordb 

def process_pdf_docs(datasource_path: str) -> list[Document]: 
    """
        processes locally stored pdf documents into a list of Document objects
    """

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


    return docs

def process_hf_ds() -> list[Document]: 
    docs =[]
    return docs

def index_documents(docs: list[Document], vectordb: VectorStore) -> IndexingResult: 
    """
        Indexes documents into a vectordb
    """

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

    return index_result

def load_knowledge_base(dataset: str): 

    vdb = get_vectordb()

    dataset_selector = {
            "MOCK": {"source": "./tests/mock_data/",  "func": process_pdf_docs,},
        "BIOASQ": {"source": "huggingface", "func": process_hf_ds}
    }
   
    try: 
        ds_conf = dataset_selector.get(dataset)
    except KeyError:
        print("Invalid DATASET value")

    processor_func = ds_conf["func"]
    docs = processor_func(ds_conf["source"])
    
    idx_results = index_documents(docs,vdb)
    print(f"Indexing Result: {idx_results}")

    
