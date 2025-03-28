# prepopulates vector embeddings into the vectordb
import itertools
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import IndexingResult, SQLRecordManager, index
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    HuggingFaceDatasetLoader,
)
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from vectordb import get_vectordb 

def process_pdf_docs(datasource_path: str) -> list[Document]: 
    """
        processes locally stored pdf documents into a list of Document objects
    """

    directory = Path(datasource_path)
    docs = []  ##type: List[Document]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=250)

    extensions  = ["*.pdf", "*.docx"]
    files = list(itertools.chain.from_iterable(directory.glob(ext) for ext in extensions))

    for file in files:
        loader = PyMuPDFLoader(str(file), mode="page")
        documents = loader.load()
        docs += text_splitter.split_documents(documents)

    if not docs: 
        print("No mock documents found in the specified directory. Exiting...")
        raise SystemExit


    return docs

def process_hf_ds(repo: str) -> list[Document]: 
    #dataset = load_dataset(repo, "text-corpus", split="test")
    docs =[]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    loader = HuggingFaceDatasetLoader(path=repo, page_content_column="passage",name="text-corpus")

    limit = 50

    documents = loader.load()
    docs += text_splitter.split_documents(documents[:limit])

    for doc in docs: 
        print(doc.metadata)

    if not docs: 
        print("No mock documents found in the specified directory. Exiting...")
        raise SystemExit


    return docs

def index_documents(docs: list[Document], vectordb: VectorStore, source_field: str) -> IndexingResult: 
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
        source_id_key=source_field,
    )

    return index_result

def load_knowledge_base(dataset: str): 

    dataset_selector = {
        "MOCK": {"source": "./data/mock_data/",  "func": process_pdf_docs,"source_field": "source"},
        "BIOASQ": {"source": "enelpol/rag-mini-bioasq", "func": process_hf_ds, "source_field": "id"},
        "PROD": {"source": "./data/prod/", "func": process_pdf_docs, "source_field": "source"}
    }

    ds_conf = dataset_selector.get(dataset)
    if not ds_conf: 
        raise KeyError("Invalid DATASET value")

    vdb = get_vectordb()

    processor_func = ds_conf["func"]
    docs = processor_func(ds_conf["source"])

    source_field = ds_conf["source_field"]
    
    idx_results = index_documents(docs,vdb, source_field)
    print(f"Indexing Result: {idx_results}")

    
